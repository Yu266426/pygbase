pub struct Timer {
    cooldown: f64,
    repeating: bool,
    time: f64,
    is_done: bool,
    is_just_done: bool,
}

#[allow(dead_code)]
impl Timer {
    pub fn new(cooldown: f64, start_done: bool, repeating: bool) -> Self {
        Self {
            cooldown,
            repeating,
            time: if start_done { 0.0 } else { cooldown },
            is_done: start_done,
            is_just_done: start_done,
        }
    }

    pub fn set_cooldown(&mut self, cooldown: f64) {
        self.cooldown = cooldown;
    }

    pub fn tick(&mut self, delta: f64) {
        self.time -= delta;

        if self.repeating {
            self.is_done = false;
            self.is_just_done = false;

            if self.time < 0.0 {
                self.time += self.cooldown;
                self.is_done = true;
                self.is_just_done = true;
            }
        } else {
            if self.time < 0.0 {
                if self.is_done {
                    self.is_just_done = false;
                } else {
                    self.is_done = true;
                    self.is_just_done = true;
                }

                self.time = 0.0;
            }
        }
    }

    pub fn start(&mut self) {
        self.time = self.cooldown;
        self.is_done = false;
        self.is_just_done = false;
    }

    pub fn finish(&mut self) {
        self.time = 0.0;
        self.is_done = true;
        self.is_just_done = true;
    }
    pub fn done(&self) -> bool {
        self.is_done
    }

    pub fn just_done(&self) -> bool {
        self.is_just_done
    }
}
