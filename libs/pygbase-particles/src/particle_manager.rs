use std::collections::HashMap;

use pyo3::{prelude::*, types::PyList};
use rand::{rngs::SmallRng, SeedableRng};

use crate::{
    particle::Particle,
    particle_spawners::{point_spawner::PointSpawner, ParticleSpawnData, ParticleSpawner},
    utils::vec2::Vec2,
};

#[pyclass]
pub struct ParticleManager {
    particles: Vec<Particle>,
    rng: SmallRng,
    spawners: HashMap<usize, Box<dyn ParticleSpawner>>,
    next_spawner_id: usize,
}

#[pymethods]
impl ParticleManager {
    #[new]
    pub fn new() -> Self {
        Self {
            particles: Vec::new(),
            rng: SmallRng::from_rng(&mut rand::rng()),
            spawners: HashMap::new(),
            next_spawner_id: 0,
        }
    }

    pub fn activate_spawner(&mut self, index: usize) -> PyResult<()> {
        self.spawners
            .get_mut(&index)
            .map(|s| s.activate())
            .ok_or_else(|| PyErr::new::<pyo3::exceptions::PyKeyError, _>(index.to_string()))?;
        Ok(())
    }

    pub fn deactivate_spawner(&mut self, index: usize) -> PyResult<()> {
        self.spawners
            .get_mut(&index)
            .map(|s| s.deactivate())
            .ok_or_else(|| PyErr::new::<pyo3::exceptions::PyKeyError, _>(index.to_string()))?;
        Ok(())
    }

    #[pyo3(signature=(pos, cooldown, amount, start_active, radial_vel_range=(0.0, 0.0)))]
    pub fn add_point_spawner(
        &mut self,
        pos: (f64, f64),
        cooldown: f64,
        amount: usize,
        start_active: bool,
        radial_vel_range: (f64, f64),
    ) -> usize {
        let spawner = PointSpawner::new(pos, cooldown, amount, start_active, radial_vel_range);
        self.add_spawner(Box::new(spawner))
    }

    pub fn add_particle(
        &mut self,
        pos: (f64, f64),
        vel: (f64, f64),
        vel_decay: f64,
        gravity: (f64, f64),
        effector: bool,
        size: f64,
        size_decay: f64,
        color: (u8, u8, u8),
    ) {
        self.particles.push(Particle::new(
            Vec2::from_tuple(pos),
            Vec2::from_tuple(vel),
            vel_decay,
            Vec2::from_tuple(gravity),
            effector,
            size,
            size_decay,
            color,
        ));
    }

    pub fn update(&mut self, delta: f64) {
        // Let every spawner emit new particles.
        let mut new_particles = Vec::new();
        for spawner in self.spawners.values_mut() {
            new_particles.extend(spawner.update(delta, &mut self.rng));
        }
        for p in new_particles {
            self.add_particle_from_data(p);
        }

        // Update existing particles.
        for particle in &mut self.particles {
            particle.update(delta);
        }

        // Drop particles that have effectively disappeared.
        self.particles.retain(|p| p.size > 0.2);
    }

    pub fn particle_positions<'py>(&self, py: Python<'py>) -> PyResult<Bound<'py, PyList>> {
        let data: Vec<(f64, f64)> = self.particles.iter().map(|p| (p.pos.x, p.pos.y)).collect();
        PyList::new(py, data)
    }

    pub fn particle_sizes<'py>(&self, py: Python<'py>) -> PyResult<Bound<'py, PyList>> {
        let data: Vec<f64> = self.particles.iter().map(|p| p.size).collect();
        PyList::new(py, data)
    }

    pub fn particle_colors<'py>(&self, py: Python<'py>) -> PyResult<Bound<'py, PyList>> {
        let data: Vec<(u8, u8, u8)> = self
            .particles
            .iter()
            .map(|p| (p.color.0, p.color.1, p.color.2))
            .collect();
        PyList::new(py, data)
    }
}

impl ParticleManager {
    fn add_particle_from_data(&mut self, data: ParticleSpawnData) {
        self.add_particle(
            data.pos,
            data.vel,
            data.vel_decay,
            data.gravity,
            data.effector,
            data.size,
            data.size_decay,
            data.color,
        );
    }

    fn add_spawner(&mut self, spawner: Box<dyn ParticleSpawner>) -> usize {
        let id = self.next_spawner_id;
        self.spawners.insert(id, spawner);
        self.next_spawner_id += 1;
        id
    }
}
