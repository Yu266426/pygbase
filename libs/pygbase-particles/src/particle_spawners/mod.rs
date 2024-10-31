use rand::rngs::SmallRng;

pub mod point_spawner;

pub trait ParticleSpawner: Send + Sync {
    fn activate(&mut self);
    fn deactivate(&mut self);
    
    fn spawn(&self, manager: &mut SmallRng) -> ParticleSpawnData;
    fn update(&mut self, delta: f64, manager: &mut SmallRng) -> Vec<ParticleSpawnData>;
}

pub struct ParticleSpawnData {
    pub pos: (f64, f64),
    pub vel: (f64, f64),
    pub vel_decay: f64,
    pub gravity: (f64, f64),
    pub effector: bool,
    pub size: f64,
    pub size_decay: f64,
    pub color: (u8, u8, u8),
}
