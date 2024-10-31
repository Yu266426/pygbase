use std::f64::consts::PI;

use rand::{rngs::SmallRng, Rng};

use crate::utils::{timer::Timer, vec2::Vec2};

use super::{ParticleSpawnData, ParticleSpawner};

pub struct PointSpawner {
    active: bool,
    pos: Vec2,
    timer: Timer,
    amount: usize,
    radial_vel_range: (f64, f64),
}

impl PointSpawner {
    pub fn new(
        pos: (f64, f64),
        cooldown: f64,
        amount: usize,
        start_active: bool,
        radial_vel_range: (f64, f64),
    ) -> Self {
        Self {
            active: start_active,
            pos: Vec2::from_tuple(pos),
            timer: Timer::new(cooldown, true, true),
            amount,
            radial_vel_range,
        }
    }
}

impl ParticleSpawner for PointSpawner {
    fn spawn(&self, rng: &mut SmallRng) -> ParticleSpawnData {
        let speed = if (self.radial_vel_range.0 - self.radial_vel_range.1).abs() < f64::EPSILON {
            0.0
        } else {
            rng.gen_range(self.radial_vel_range.0..self.radial_vel_range.1)
        };
        let angle = rng.gen_range(0.0..(2.0 * PI));

        let vel = (angle.cos() * speed, angle.sin() * speed);

        let vel_decay = rng.gen_range(1.2..2.3);
        let size = rng.gen_range(4.0..6.0);
        let size_decay = rng.gen_range(2.0..4.0);
        
        let color = (
            rng.gen_range(0..255),
            rng.gen_range(0..255),
            rng.gen_range(0..255),
        );

        ParticleSpawnData {
            pos: self.pos.into(),
            vel,
            vel_decay,
            gravity: (0.0, 0.0),
            effector: false,
            size,
            size_decay,
            color,
        }
    }

    fn update(&mut self, delta: f64, rng: &mut SmallRng) -> Vec<ParticleSpawnData> {
        let mut particle_spawn_data = Vec::new();

        if self.active {
            self.timer.tick(delta);

            if self.timer.done() {
                for _ in 0..self.amount {
                    particle_spawn_data.push(self.spawn(rng));
                }
            }
        }

        particle_spawn_data
    }

    fn activate(&mut self) {
        self.active = true;
    }

    fn deactivate(&mut self) {
        self.active = false;
    }
}
