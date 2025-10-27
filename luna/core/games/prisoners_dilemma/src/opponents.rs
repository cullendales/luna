use rand::Rng;

const opponents = [&str; 15] = [
    "random",
    "unconditional_cooperator",
    "always_betray",
    "tit_for_tat",
    "suspicious_tit_for_tat",
    "gradual_tit_for_tat",
    "imperfect_tit_for_tat",
    "tit_for_tat_betray_last",
    "triggered",
    "even_steven",
    "odd_todd",
    "fibonacci",
    "friends_for_two", //pos for two neg for two
    "opposite",
    "betrays_if_friendly",
]

fn get_opponent() -> &str {
    let opponent_num = rand::Rng().random_range(0..10);
    let opponent = opponents[opponent_num];
    opponent
}