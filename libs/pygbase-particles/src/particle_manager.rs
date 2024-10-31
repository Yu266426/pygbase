use std::collections::HashMap;

use pyo3::{
    prelude::*,
    types::{PyList, PyTuple},
};
use rand::{rngs::SmallRng, SeedableRng};

use crate::{
    particle::Particle,
    particle_spawners::{point_spawner::PointSpawner, ParticleSpawnData, ParticleSpawner},
    utils::vec2::Vec2,
};

#[pyclass]
pub struct ParticleManager {
    particles: Vec<Particle>,
    pub rng: SmallRng,
    spawners: HashMap<usize, Box<dyn ParticleSpawner>>,
    spawner_index: usize,
}

#[pymethods]
impl ParticleManager {
    #[new]
    pub fn new() -> Self {
        Self {
            particles: Vec::new(),
            rng: SmallRng::from_entropy(),
            spawners: HashMap::new(),
            spawner_index: 0,
        }
    }

    pub fn activate_spawner(&mut self, index: usize) {
        if let Some(spawner) = self.spawners.get_mut(&index) {
            spawner.as_mut().activate();
        }
        // TODO: add error if not found here
    }

    pub fn deactivate_spawner(&mut self, index: usize) {
        if let Some(spawner) = self.spawners.get_mut(&index) {
            spawner.as_mut().deactivate();
        }
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
        let mut particles_to_spawn = Vec::new();
        for (_index, spawner) in &mut self.spawners {
            particles_to_spawn.extend(spawner.as_mut().update(delta, &mut self.rng));
        }

        for particle in particles_to_spawn {
            self.add_particle_from_struct(particle);
        }

        for particle in &mut self.particles {
            particle.update(delta);
        }

        self.particles.retain(|e| e.size > 0.2);
    }

    pub fn get_particle_positions<'py>(&self, py: Python<'py>) -> PyResult<Bound<'py, PyList>> {
        let positions: Vec<Bound<PyTuple>> = self
            .particles
            .iter()
            .map(|e| PyTuple::new_bound(py, vec![e.pos.x, e.pos.y]))
            .collect();

        Ok(PyList::new_bound(py, positions))
    }

    pub fn get_particle_sizes<'py>(&self, py: Python<'py>) -> PyResult<Bound<'py, PyList>> {
        let sizes: Vec<f64> = self.particles.iter().map(|e| e.size).collect();

        Ok(PyList::new_bound(py, sizes))
    }

    pub fn get_particle_colors<'py>(&self, py: Python<'py>) -> PyResult<Bound<'py, PyList>> {
        let colors: Vec<Bound<PyTuple>> = self
            .particles
            .iter()
            .map(|e| PyTuple::new_bound(py, vec![e.color.0, e.color.1, e.color.2]))
            .collect();

        Ok(PyList::new_bound(py, colors))
    }
}

impl ParticleManager {
    fn add_particle_from_struct(&mut self, particle: ParticleSpawnData) {
        self.add_particle(
            particle.pos,
            particle.vel,
            particle.vel_decay,
            particle.gravity,
            particle.effector,
            particle.size,
            particle.size_decay,
            particle.color,
        );
    }

    fn add_spawner(&mut self, spawner: Box<dyn ParticleSpawner>) -> usize {
        self.spawners.insert(self.spawner_index, spawner);
        self.spawner_index += 1;
        self.spawner_index - 1
    }
}
