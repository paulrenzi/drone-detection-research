// 3D viewer for the CAD page: rotate, zoom, scrub between assembled and exploded,
// and name the part under the pointer. One <div class="cad-viewer"> per model:
//   data-src        .glb with an "explode" animation clip (or the assembled model)
//   data-exploded   optional second .glb, used when the file carries no animation
//   data-manifest   manifest.json URL, data-model = its key for this model
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

const manifests = {};
function loadManifest(url) {
  if (!url) return Promise.resolve(null);
  if (!manifests[url]) manifests[url] = fetch(url).then(r => r.ok ? r.json() : null).catch(() => null);
  return manifests[url];
}

function partsFor(manifest, key) {
  if (!manifest) return {};
  const models = manifest.models || manifest;
  const m = Array.isArray(models) ? models.find(x => x.name === key || x.key === key) : models[key];
  const list = (m && (m.parts || m.nodes)) || [];
  const byNode = {};
  for (const p of list) byNode[p.node || p.node_name || p.name] = p;
  return byNode;
}

function el(tag, cls, text) {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (text != null) e.textContent = text;
  return e;
}

function boxOf(obj) {
  obj.updateMatrixWorld(true);
  return new THREE.Box3().setFromObject(obj);
}

async function setup(root) {
  let needsRender = true, visible = true;
  const stage = el('div', 'cad-stage');
  const tip = el('div', 'cad-tip');
  const status = el('div', 'cad-status', 'Loading model…');
  stage.append(status, tip);

  const bar = el('div', 'cad-bar');
  const bAsm = el('button', 'cad-btn is-on', 'Assembled');
  const bExp = el('button', 'cad-btn', 'Exploded');
  const slider = el('input', 'cad-slider');
  Object.assign(slider, { type: 'range', min: 0, max: 1000, value: 0 });
  slider.setAttribute('aria-label', 'Explode amount');
  const bReset = el('button', 'cad-btn', 'Reset view');
  bar.append(bAsm, bExp, slider, bReset);
  const info = el('div', 'cad-info', 'Drag to rotate, scroll or pinch to zoom, right-drag to pan. Point at a part to name it.');
  root.append(stage, bar, info);

  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  } catch (e) {
    status.textContent = 'This browser cannot show 3D (WebGL is off). The renders below show the same model.';
    bar.remove();
    return;
  }
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.toneMapping = THREE.NeutralToneMapping;
  renderer.toneMappingExposure = 0.9;
  stage.prepend(renderer.domElement);

  const scene = new THREE.Scene();
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
  scene.environmentIntensity = 0.45;
  const sun = new THREE.DirectionalLight(0xffffff, 1.6);
  sun.position.set(2, 4, 3);
  scene.add(sun);

  const camera = new THREE.PerspectiveCamera(35, 1, 0.001, 100);
  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;

  const loader = new GLTFLoader();
  const [manifest, gltf, gltfExp] = await Promise.all([
    loadManifest(root.dataset.manifest),
    loader.loadAsync(root.dataset.src),
    root.dataset.exploded ? loader.loadAsync(root.dataset.exploded) : Promise.resolve(null),
  ]).catch(err => {
    status.textContent = 'The model failed to load: ' + err.message;
    return [];
  });
  if (!gltf) return;
  status.remove();
  const parts = partsFor(manifest, root.dataset.model);

  const model = gltf.scene;
  scene.add(model);
  let modelExp = null;
  let mixer = null, action = null, duration = 0;
  const clip = gltf.animations.find(a => a.name === 'explode') || gltf.animations[0];
  if (clip) {
    mixer = new THREE.AnimationMixer(model);
    action = mixer.clipAction(clip);
    action.setLoop(THREE.LoopOnce);
    action.clampWhenFinished = true;
    action.play();
    action.paused = true;
    duration = clip.duration;
  } else if (gltfExp) {
    modelExp = gltfExp.scene;
    modelExp.visible = false;
    scene.add(modelExp);
  } else {
    bAsm.remove(); bExp.remove(); slider.remove();
  }

  function setExplode(t) {
    if (mixer) {
      action.time = t * duration;
      mixer.update(0);
    } else if (modelExp) {
      model.visible = t < 0.5;
      modelExp.visible = t >= 0.5;
    }
    bAsm.classList.toggle('is-on', t < 0.5);
    bExp.classList.toggle('is-on', t >= 0.5);
    needsRender = true;
  }

  // Frame the camera on both states so exploding never runs off screen.
  const box = boxOf(model);
  setExplode(1);
  box.union(boxOf(modelExp && modelExp.visible ? modelExp : model));
  setExplode(0);
  const centre = box.getCenter(new THREE.Vector3());
  const viewDir = new THREE.Vector3(0.45, 0.55, 1).normalize();
  // Distance at which all eight box corners fit the current aspect, plus a margin.
  function fitDistance() {
    const look = new THREE.Matrix4().lookAt(viewDir, new THREE.Vector3(), new THREE.Vector3(0, 1, 0));
    const inv = look.clone().invert();
    const tanV = Math.tan(THREE.MathUtils.degToRad(camera.fov / 2)), tanH = tanV * camera.aspect;
    let d = 0;
    for (let i = 0; i < 8; i++) {
      const c = new THREE.Vector3(i & 1 ? box.max.x : box.min.x, i & 2 ? box.max.y : box.min.y, i & 4 ? box.max.z : box.min.z)
        .sub(centre).applyMatrix4(inv);
      d = Math.max(d, c.z + Math.abs(c.x) / tanH, c.z + Math.abs(c.y) / tanV);
    }
    return d * 1.08;
  }
  function resetView() {
    const dist = fitDistance();
    camera.near = dist / 100;
    camera.far = dist * 20;
    camera.updateProjectionMatrix();
    camera.position.copy(centre).addScaledVector(viewDir, dist);
    controls.target.copy(centre);
    controls.update();
    needsRender = true;
  }


  let anim = null;
  function animateTo(target) {
    const from = slider.value / 1000, start = performance.now(), ms = 900;
    anim = now => {
      const k = Math.min(1, (now - start) / ms);
      const e = k < 0.5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2;
      const t = from + (target - from) * e;
      slider.value = Math.round(t * 1000);
      setExplode(t);
      if (k >= 1) anim = null;
    };
  }
  bAsm.onclick = () => animateTo(0);
  bExp.onclick = () => animateTo(1);
  slider.oninput = () => { anim = null; setExplode(slider.value / 1000); };
  bReset.onclick = resetView;

  // Name the part under the pointer: walk up to the nearest node the manifest knows,
  // or failing that the nearest named node below the scene root.
  const ray = new THREE.Raycaster(), ptr = new THREE.Vector2();
  let lit = null;
  const litMats = new Map();
  function partOf(obj, top) {
    let fallback = null;
    for (let o = obj; o && o !== top; o = o.parent) {
      if (parts[o.name]) return { node: o, info: parts[o.name] };
      if (o.name && o.parent === top) fallback = o;
      if (o.name && !fallback && !o.isMesh) fallback = o;
    }
    return fallback ? { node: fallback, info: null } : null;
  }
  function highlight(node) {
    if (lit === node) return;
    for (const [m, c] of litMats) m.emissive && m.emissive.copy(c);
    litMats.clear();
    lit = node;
    if (node) node.traverse(o => {
      if (!o.isMesh) return;
      for (const m of [].concat(o.material)) {
        if (!m.emissive || litMats.has(m)) continue;
        litMats.set(m, m.emissive.clone());
        m.emissive.setRGB(0.25, 0.18, 0.02);
      }
    });
    needsRender = true;
  }
  function pick(ev, click) {
    const r = renderer.domElement.getBoundingClientRect();
    ptr.set(((ev.clientX - r.left) / r.width) * 2 - 1, -((ev.clientY - r.top) / r.height) * 2 + 1);
    ray.setFromCamera(ptr, camera);
    const live = modelExp && modelExp.visible ? modelExp : model;
    const hit = ray.intersectObject(live, true)[0];
    const p = hit && partOf(hit.object, live);
    highlight(p ? p.node : null);
    if (!p) { tip.style.display = 'none'; return; }
    const name = (p.info && (p.info.display_name || p.info.display)) || p.node.name.replace(/_/g, ' ');
    const kind = p.info && (p.info.printed_or_bought || p.info.kind || (p.info.printed === true ? 'printed' : p.info.printed === false ? 'bought' : ''));
    tip.textContent = kind ? `${name} · ${kind}` : name;
    tip.style.display = 'block';
    tip.style.left = (ev.clientX - r.left + 14) + 'px';
    tip.style.top = (ev.clientY - r.top + 14) + 'px';
    if (click && p.info) {
      const bits = [name];
      if (p.info.mass_g != null) bits.push(`${(+p.info.mass_g).toFixed(1)} g`);
      const what = p.info.function || p.info.description;
      info.textContent = bits.join(' · ') + (what ? ` — ${what}` : '');
    }
  }
  renderer.domElement.addEventListener('pointermove', ev => { if (ev.buttons === 0) pick(ev, false); });
  renderer.domElement.addEventListener('pointerup', ev => pick(ev, true));
  renderer.domElement.addEventListener('pointerleave', () => { tip.style.display = 'none'; highlight(null); });

  controls.addEventListener('change', () => { needsRender = true; });
  new IntersectionObserver(es => { visible = es[0].isIntersecting; }).observe(root);
  function resize() {
    const w = stage.clientWidth, h = stage.clientHeight;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    needsRender = true;
  }
  new ResizeObserver(resize).observe(stage);
  resize();
  resetView();
  renderer.setAnimationLoop(now => {
    if (!visible) return;
    if (anim) anim(now);
    controls.update();
    if (needsRender) { renderer.render(scene, camera); needsRender = false; }
  });
}

document.querySelectorAll('.cad-viewer').forEach(root => setup(root).catch(err => {
  root.textContent = 'The 3D viewer failed: ' + err.message;
}));
