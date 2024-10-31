use crate::utils::vec2::Vec2;

pub struct Particle {
    pub pos: Vec2,
    pub velocity: Vec2,
    pub velocity_decay: f64,
    pub gravity: Vec2,
    pub effector: bool,
    pub size: f64,
    pub size_decay: f64,
    pub color: (u8, u8, u8),
}

impl Particle {
    pub fn new(
        pos: Vec2,
        velocity: Vec2,
        velocity_decay: f64,
        gravity: Vec2,
        effector: bool,
        size: f64,
        size_decay: f64,
        color: (u8, u8, u8),
    ) -> Self {
        Self {
            pos,
            velocity,
            velocity_decay,
            gravity,
            effector,
            size,
            size_decay,
            color,
        }
    }

    pub fn update(&mut self, delta: f64) {
        self.velocity += self.gravity * delta;
        self.velocity -= self.velocity * self.velocity_decay * delta;

        self.pos += self.velocity * delta;
        self.size -= self.size_decay * delta;
    }
}
