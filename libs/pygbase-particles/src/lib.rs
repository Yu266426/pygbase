use pyo3::prelude::*;

mod particle;
mod particle_manager;
mod particle_spawners;
mod particle_settings;
mod utils;

use particle_manager::ParticleManager;

#[pymodule]
fn pygbase_particles(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<ParticleManager>()?;
    Ok(())
}
