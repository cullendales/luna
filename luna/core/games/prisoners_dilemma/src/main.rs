use pyo3::prelude::*;
use pyo3::types::PyModule;

fn battle(opponent: &str) -> &str {
    Python::with_gil(|py|{
        let module = PyModule::import(py, "text_and_audio.stt")?;
    })
}


fn begin_prisoners_dilemma() {
    let rival = get_opponent();
    battle(opponent);
}
