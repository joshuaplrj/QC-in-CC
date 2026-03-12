// WebGL 3D Quantum Engine Controller

const QuantumEngine3D = {
    scene: null,
    camera: null,
    renderer: null,
    controls: null,
    clock: null,
    currentAnimation: null,
    systemData: null,
    
    // Engine State
    frameCount: 0,
    lastFpsTime: 0,

    init(systemKey) {
        this.clock = new THREE.Clock();
        
        // Setup Three.js Scene
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0x050a12); // match css
        
        // Add subtle fog for depth
        this.scene.fog = new THREE.FogExp2(0x050a12, 0.0015);
        
        // Setup Camera
        const aspect = window.innerWidth / window.innerHeight;
        this.camera = new THREE.PerspectiveCamera(60, aspect, 0.1, 2000);
        this.camera.position.set(0, 50, 150);
        
        // Setup Renderer
        const container = document.getElementById('canvas-container');
        this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.setPixelRatio(window.devicePixelRatio);
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        container.appendChild(this.renderer.domElement);
        
        // Setup OrbitControls
        this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
        this.controls.enableDamping = true;
        this.controls.dampingFactor = 0.05;
        this.controls.maxDistance = 600;
        
        // Setup Lighting (Beautiful Studio Lighting setup)
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.3); // Soft base
        this.scene.add(ambientLight);
        
        const mainDirLight = new THREE.DirectionalLight(0xffffff, 0.8);
        mainDirLight.position.set(100, 200, 100);
        mainDirLight.castShadow = true;
        mainDirLight.shadow.mapSize.width = 2048;
        mainDirLight.shadow.mapSize.height = 2048;
        this.scene.add(mainDirLight);
        
        const rimLight = new THREE.DirectionalLight(0x38bdf8, 0.5); // Quantum blue rim
        rimLight.position.set(-100, 50, -100);
        this.scene.add(rimLight);
        
        const accentLight = new THREE.PointLight(0xf43f5e, 0.6, 300); // Danger red accent
        accentLight.position.set(50, 20, 50);
        this.scene.add(accentLight);

        // Handle Resizing
        window.addEventListener('resize', this.onWindowResize.bind(this), false);
        
        // Load the requested system
        this.loadSystem(systemKey);
        
        // Start Render Loop
        this.lastFpsTime = performance.now();
        this.animate();
    },
    
    loadSystem(key) {
        this.systemData = SystemRegistry[key] || SystemRegistry['default'];
        
        // Update UI HTML
        document.getElementById('system-title').innerText = this.systemData.title;
        document.getElementById('system-desc').innerHTML = this.systemData.description;
        document.getElementById('metric-vqe').innerText = this.systemData.solverType || "Active";
        
        // Clean scene if needed
        this.clearCustomMeshes();
        
        // Initialize the specific animation
        if (this.systemData.init) {
            this.currentAnimation = this.systemData;
            this.currentAnimation.init(this.scene, this.camera);
        }
    },
    
    clearCustomMeshes() {
        // Remove everything except lights and camera
        const toRemove = [];
        this.scene.traverse((child) => {
            if (child.isMesh || child.isLine || child.isPoints || child.isGroup) {
                // Don't accidentally wipe out lights or helpers if they have meshes attached, though rare
                toRemove.push(child);
            }
        });
        
        toRemove.forEach(object => {
            this.scene.remove(object);
            if (object.geometry) object.geometry.dispose();
            if (object.material) {
                if (Array.isArray(object.material)) {
                    object.material.forEach(m => m.dispose());
                } else {
                    object.material.dispose();
                }
            }
        });
    },
    
    onWindowResize() {
        this.camera.aspect = window.innerWidth / window.innerHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(window.innerWidth, window.innerHeight);
    },
    
    animate() {
        requestAnimationFrame(this.animate.bind(this));
        
        const delta = this.clock.getDelta();
        const time = this.clock.getElapsedTime();
        
        this.controls.update(); // only required if controls.enableDamping or controls.autoRotate are set
        
        // Call specific animation tick
        if (this.currentAnimation && this.currentAnimation.tick) {
            this.currentAnimation.tick(time, delta);
        }
        
        this.renderer.render(this.scene, this.camera);
        
        // Simple FPS tracking
        this.frameCount++;
        const now = performance.now();
        if (now - this.lastFpsTime >= 500) {
            const fps = Math.round((this.frameCount * 1000) / (now - this.lastFpsTime));
            document.getElementById('metric-fps').innerText = fps + " FPS";
            this.frameCount = 0;
            this.lastFpsTime = now;
        }
    }
};

// Utilities for colors matching the Python palette
const Palette = {
    primary: 0x38bdf8,   // VQE Blue
    secondary: 0xc4b5fd, // QAOA Purple
    accent: 0x34d399,    // HHL Green
    danger: 0xf43f5e,    // Error/Hot Red
    muted: 0x64748b,
    grid: 0x334155,
    gold: 0xfbbf24
};
