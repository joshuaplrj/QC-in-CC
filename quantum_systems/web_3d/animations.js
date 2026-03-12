// Animation Definitions for Quantum Engine 3D

const SystemRegistry = {
    'default': {
        title: "Quantum System Not Found",
        description: "Please launch from the Quantum Dashboard.",
        solverType: "Idle",
        init(scene, camera) {
            // Draw simple rotating cube
            const geo = new THREE.BoxGeometry(20, 20, 20);
            const mat = new THREE.MeshStandardMaterial({ color: Palette.muted });
            this.mesh = new THREE.Mesh(geo, mat);
            scene.add(this.mesh);
        },
        tick(time, delta) {
            if (this.mesh) {
                this.mesh.rotation.x = time;
                this.mesh.rotation.y = time;
            }
        }
    },

    // 1. Robot Kinematics (Mechanical Engineering)
    'robot_kinematics': {
        title: "Robot Kinematics",
        description: "QAOA calculated 3D inverse kinematics mapping a 6-DoF robotic arm trajectory.",
        solverType: "QAOA Optimization",
        init(scene, camera) {
            // Setup Arm hierarchy
            this.base = new THREE.Group();
            scene.add(this.base);

            const matPrimary = new THREE.MeshStandardMaterial({ color: 0x1a2b3d, roughness: 0.4, metalness: 0.8 });
            const matJoint = new THREE.MeshStandardMaterial({ color: Palette.primary, roughness: 0.2, metalness: 0.9 });
            const matTarget = new THREE.MeshStandardMaterial({ color: Palette.danger, wireframe: true });

            // Base stand
            const baseGeo = new THREE.CylinderGeometry(20, 25, 10, 32);
            const baseMesh = new THREE.Mesh(baseGeo, matPrimary);
            baseMesh.position.y = 5;
            this.base.add(baseMesh);

            // Joint 1 (Shoulder Yaw)
            this.j1 = new THREE.Group();
            this.j1.position.y = 10;
            this.base.add(this.j1);

            const j1Mesh = new THREE.Mesh(new THREE.CylinderGeometry(15, 15, 20, 32), matJoint);
            j1Mesh.rotation.x = Math.PI / 2;
            this.j1.add(j1Mesh);

            // Link 1
            const l1Geo = new THREE.BoxGeometry(10, 60, 10);
            const l1Mesh = new THREE.Mesh(l1Geo, matPrimary);
            l1Mesh.position.y = 30; // center of link
            this.j1.add(l1Mesh);

            // Joint 2 (Elbow Pitch)
            this.j2 = new THREE.Group();
            this.j2.position.y = 60; // relative to j1
            this.j1.add(this.j2);

            const j2Mesh = new THREE.Mesh(new THREE.CylinderGeometry(12, 12, 15, 32), matJoint);
            j2Mesh.rotation.z = Math.PI / 2;
            this.j2.add(j2Mesh);

            // Link 2
            const l2Geo = new THREE.BoxGeometry(8, 50, 8);
            const l2Mesh = new THREE.Mesh(l2Geo, matPrimary);
            l2Mesh.position.y = 25;
            this.j2.add(l2Mesh);

            // Joint 3 (Wrist Pitch)
            this.j3 = new THREE.Group();
            this.j3.position.y = 50;
            this.j2.add(this.j3);

            const j3Mesh = new THREE.Mesh(new THREE.SphereGeometry(8, 16, 16), matJoint);
            this.j3.add(j3Mesh);

            // End Effector
            const eeGeo = new THREE.ConeGeometry(4, 15, 4);
            const eeMesh = new THREE.Mesh(eeGeo, matPrimary);
            eeMesh.position.y = 7.5;
            this.j3.add(eeMesh);

            // Target Point
            this.target = new THREE.Mesh(new THREE.SphereGeometry(5, 16, 16), matTarget);
            scene.add(this.target);

            // Grid Floor
            const grid = new THREE.GridHelper(200, 20, Palette.grid, 0x111111);
            scene.add(grid);

            // Reset camera for this view
            camera.position.set(100, 80, 150);
            camera.lookAt(0, 50, 0);
        },
        tick(time, delta) {
            // Move target in a 3D figure-8 pattern (Lissajous curve)
            const tx = Math.sin(time) * 40;
            const ty = 60 + Math.sin(time * 2) * 30;
            const tz = Math.cos(time * 1.5) * 40 + 40;

            this.target.position.set(tx, ty, tz);

            // Simple Inverse Kinematics approximation for visualization
            // Base look at target XZ
            const targetAngleY = Math.atan2(tx, tz);
            this.j1.rotation.y = targetAngleY;

            // Planar IK for J2 and J3
            const distXZ = Math.hypot(tx, tz);
            const targetDist = Math.hypot(distXZ, ty - 10);

            const l1 = 60;
            const l2 = 50;

            // Law of cosines safely clamped
            let cosAngle2 = (targetDist * targetDist - l1 * l1 - l2 * l2) / (2 * l1 * l2);
            cosAngle2 = Math.max(-1, Math.min(1, cosAngle2));
            const angle2 = Math.acos(cosAngle2); // Elbow angle (relative)

            // Shoulder elevation angle
            const elevation = Math.atan2(ty - 10, distXZ);
            // Internal angle at shoulder
            let cosAngle1 = (targetDist * targetDist + l1 * l1 - l2 * l2) / (2 * targetDist * l1);
            cosAngle1 = Math.max(-1, Math.min(1, cosAngle1));
            const angle1 = Math.acos(cosAngle1);

            this.j1.rotation.x = (Math.PI / 2) - (elevation + angle1);
            this.j2.rotation.x = angle2;

            // Keep effector pointing generally down/forward
            this.j3.rotation.x = -(this.j1.rotation.x + this.j2.rotation.x) - Math.PI / 4;
        }
    },

    // 2. Molecular Dynamics (Materials Science)
    'molecular_dynamics': {
        title: "Molecular Dynamics",
        description: "VQE resolving 3x3x3 3D crystalline lattice structure thermal variations in real-time.",
        solverType: "VQE Hamiltonian",
        init(scene, camera) {
            this.atoms = [];
            this.bonds = [];
            this.group = new THREE.Group();
            scene.add(this.group);

            const grid = new THREE.GridHelper(200, 10, Palette.grid, Palette.grid);
            grid.position.y = -60;
            scene.add(grid);

            // Crystal Lattice
            const spacing = 30;
            const atomGeo = new THREE.SphereGeometry(6, 32, 32);

            // Standard materials
            this.matCool = new THREE.MeshPhysicalMaterial({
                color: Palette.primary, metalness: 0.1, roughness: 0.2, transmission: 0.5, thickness: 1.5
            });
            this.matHot = new THREE.MeshPhysicalMaterial({
                color: Palette.danger, metalness: 0.1, roughness: 0.2, transmission: 0.5, thickness: 1.5
            });

            this.bondMat = new THREE.MeshStandardMaterial({ color: Palette.secondary, roughness: 0.5 });
            const bondGeo = new THREE.CylinderGeometry(1.5, 1.5, 1, 8); // length updated dynamically

            // Create 3x3x3 grid
            for (let x = -1; x <= 1; x++) {
                for (let y = -1; y <= 1; y++) {
                    for (let z = -1; z <= 1; z++) {
                        const mesh = new THREE.Mesh(atomGeo, this.matCool);
                        mesh.position.set(x * spacing, y * spacing, z * spacing);
                        // Save logical index coordinates for physics
                        mesh.userData = { x, y, z, base: new THREE.Vector3(x * spacing, y * spacing, z * spacing) };
                        this.group.add(mesh);
                        this.atoms.push(mesh);
                    }
                }
            }

            // Create Bonds (Lines connecting adjacent atoms)
            for (let i = 0; i < this.atoms.length; i++) {
                for (let j = i + 1; j < this.atoms.length; j++) {
                    const a1 = this.atoms[i];
                    const a2 = this.atoms[j];

                    // Connected if distance == spacing
                    const dist = a1.userData.base.distanceTo(a2.userData.base);
                    if (Math.abs(dist - spacing) < 1.0) {
                        const bond = new THREE.Mesh(bondGeo, this.bondMat);
                        this.group.add(bond);
                        this.bonds.push({ mesh: bond, a1: a1, a2: a2 });
                    }
                }
            }

            // Centralize camera
            camera.position.set(80, 80, 120);
            camera.lookAt(0, 0, 0);
        },
        tick(time, delta) {
            // Global rotation
            this.group.rotation.y = time * 0.2;
            this.group.rotation.z = Math.sin(time * 0.1) * 0.2;

            // Thermal fluctuation phase
            const temp = 0.5 + 0.5 * Math.sin(time * 0.5); // 0 to 1
            const activeMat = temp > 0.6 ? this.matHot : this.matCool;

            // Jitter atoms
            for (let atom of this.atoms) {
                atom.material = activeMat;
                const phase_offset = atom.userData.x * 7 + atom.userData.y * 11 + atom.userData.z * 13;

                // Displacement scales with temp
                const dx = Math.sin(time * 5 + phase_offset) * 5 * temp;
                const dy = Math.cos(time * 4.3 + phase_offset) * 5 * temp;
                const dz = Math.sin(time * 3.7 + phase_offset) * 5 * temp;

                atom.position.copy(atom.userData.base).add(new THREE.Vector3(dx, dy, dz));
            }

            // Update bonds to span between jittering atoms
            for (let b of this.bonds) {
                const p1 = b.a1.position;
                const p2 = b.a2.position;

                const distance = p1.distanceTo(p2);
                b.mesh.position.copy(p1).lerp(p2, 0.5);
                b.mesh.scale.set(1, distance, 1);

                b.mesh.quaternion.setFromUnitVectors(
                    new THREE.Vector3(0, 1, 0),
                    p2.clone().sub(p1).normalize()
                );
            }
        }
    },

    // 3. Reactor Design (Chemical Engineering)
    'reactor_design': {
        title: "CSTR Reactor Design",
        description: "VQE real-time fluid particle mixing within a Continuous Stirred Tank Reactor in 3D.",
        solverType: "VQE Hamiltonian",
        init(scene, camera) {
            this.group = new THREE.Group();
            scene.add(this.group);

            // Transparent Glass Tank
            const tankGeo = new THREE.CylinderGeometry(40, 40, 100, 32, 1, true); // Open ends
            const tankMat = new THREE.MeshPhysicalMaterial({
                color: 0xaaaaaa, transmission: 0.9, opacity: 1, metalness: 0, roughness: 0.1, side: THREE.DoubleSide
            });
            const tank = new THREE.Mesh(tankGeo, tankMat);
            this.group.add(tank);

            // Tank caps (wireframe so we can see inside)
            const capGeo = new THREE.CircleGeometry(40, 32);
            const capMat = new THREE.MeshBasicMaterial({ color: Palette.grid, wireframe: true });

            const topCap = new THREE.Mesh(capGeo, capMat);
            topCap.rotation.x = -Math.PI / 2;
            topCap.position.y = 50;
            this.group.add(topCap);

            const botCap = new THREE.Mesh(capGeo, capMat);
            botCap.rotation.x = Math.PI / 2;
            botCap.position.y = -50;
            this.group.add(botCap);

            // Central Impeller Shaft
            const shaftGeo = new THREE.CylinderGeometry(2, 2, 120, 16);
            const shaftMat = new THREE.MeshStandardMaterial({ color: Palette.secondary, metalness: 0.8 });
            this.shaft = new THREE.Mesh(shaftGeo, shaftMat);
            this.group.add(this.shaft);

            // Impeller Blades
            this.blades = new THREE.Group();
            this.blades.position.y = -20;
            this.shaft.add(this.blades);

            const bladeGeo = new THREE.BoxGeometry(60, 10, 2);
            const b1 = new THREE.Mesh(bladeGeo, shaftMat);
            b1.rotation.x = Math.PI / 6; // pitch
            const b2 = new THREE.Mesh(bladeGeo, shaftMat);
            b2.rotation.y = Math.PI / 2;
            b2.rotation.x = Math.PI / 6;
            this.blades.add(b1);
            this.blades.add(b2);

            // Particle System (Reactants A + B -> C)
            const particleCount = 200;
            this.particles = new THREE.InstancedMesh(
                new THREE.SphereGeometry(2, 8, 8),
                new THREE.MeshStandardMaterial({ color: 0xffffff }), // base color overridden by instance color
                particleCount
            );
            this.group.add(this.particles);

            this.particleData = [];
            for (let i = 0; i < particleCount; i++) {
                this.particleData.push({
                    radius: Math.random() * 35,
                    angle: Math.random() * Math.PI * 2,
                    y: (Math.random() * 90) - 45, // -45 to 45
                    type: Math.random() > 0.5 ? 0 : 1, // 0=A, 1=B
                    converted: false,
                    speedY: (Math.random() - 0.5) * 0.5
                });
            }

            // Colors
            this.colA = new THREE.Color(Palette.primary);
            this.colB = new THREE.Color(Palette.danger);
            this.colC = new THREE.Color(Palette.accent);

            camera.position.set(0, 30, 150);
        },
        tick(time, delta) {
            // Spin impeller
            this.shaft.rotation.y += delta * 5; // Fast spin

            // Slightly auto-rotate the whole assembly to show off 3D
            this.group.rotation.x = Math.sin(time * 0.5) * 0.1;
            this.group.rotation.z = Math.cos(time * 0.5) * 0.05;

            // Update particles
            const dummy = new THREE.Object3D();

            for (let i = 0; i < this.particles.count; i++) {
                let p = this.particleData[i];

                // Vortex physics
                // Faster near bottom blade (y=-20)
                const distToBlade = Math.abs(p.y - (-20));
                const vortexStrength = Math.max(0.2, 1.0 - (distToBlade / 80.0));

                p.angle += delta * 3 * vortexStrength;

                // Vertical mixing
                p.y += p.speedY;
                if (p.y > 45) { p.y = 45; p.speedY *= -1; }
                if (p.y < -45) { p.y = -45; p.speedY *= -1; }

                // Reaction logic
                // Reactants spend time in the high mixing zone near blades to convert
                if (!p.converted && distToBlade < 20) {
                    if (Math.random() < 0.05) { // 5% chance per frame in active zone
                        p.converted = true;
                    }
                }

                // Plot matrix
                dummy.position.set(
                    Math.cos(p.angle) * p.radius,
                    p.y,
                    Math.sin(p.angle) * p.radius
                );
                dummy.updateMatrix();
                this.particles.setMatrixAt(i, dummy.matrix);

                // Set Color
                if (p.converted) {
                    this.particles.setColorAt(i, this.colC);
                } else {
                    this.particles.setColorAt(i, p.type === 0 ? this.colA : this.colB);
                }
            }
            this.particles.instanceMatrix.needsUpdate = true;
            this.particles.instanceColor.needsUpdate = true;
        }
    }
};
