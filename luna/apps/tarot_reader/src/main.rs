use rand::Rng;
use std::error::Error;
use std::fs::File;
use std::path::Path;
use viuer::{Config, print_from_file};
use image::{DynamicImage, Rgba};
use imageproc::geometric_transformations::{rotate_about_center, Interpolation};
use std::io::{self, Write};


const TAROT_CARDS: [&str; 78] = [
    "The Fool", 
    "The Magician", 
    "The High Priestess", 
    "The Empress",
    "The Emperor", 
    "The Hierophant", 
    "The Lovers", 
    "The Chariot",
    "Strength", 
    "The Hermit", 
    "Wheel of Fortune", 
    "Justice",
    "The Hanged Man", 
    "Death", 
    "Temperance", 
    "The Devil",
    "The Tower", 
    "The Star", 
    "The Moon", 
    "The Sun",
    "Judgement", 
    "The World",
    "Ace of Wands", 
    "Two of Wands", 
    "Three of Wands", 
    "Four of Wands",
    "Five of Wands", 
    "Six of Wands", 
    "Seven of Wands",
    "Eight of Wands",
    "Nine of Wands", 
    "Ten of Wands", 
    "Page of Wands", 
    "Knight of Wands",
    "Queen of Wands", 
    "King of Wands",
    "Ace of Cups", 
    "Two of Cups", 
    "Three of Cups",
    "Four of Cups",
    "Five of Cups", 
    "Six of Cups", 
    "Seven of Cups", 
    "Eight of Cups",
    "Nine of Cups", 
    "Ten of Cups", 
    "Page of Cups", 
    "Knight of Cups",
    "Queen of Cups", 
    "King of Cups",
    "Ace of Swords", 
    "Two of Swords", 
    "Three of Swords", 
    "Four of Swords",
    "Five of Swords", 
    "Six of Swords", 
    "Seven of Swords", 
    "Eight of Swords",
    "Nine of Swords", 
    "Ten of Swords", 
    "Page of Swords", 
    "Knight of Swords",
    "Queen of Swords", 
    "King of Swords",
    "Ace of Pentacles", 
    "Two of Pentacles", 
    "Three of Pentacles", 
    "Four of Pentacles",
    "Five of Pentacles", 
    "Six of Pentacles", 
    "Seven of Pentacles", 
    "Eight of Pentacles",
    "Nine of Pentacles",
    "Ten of Pentacles", 
    "Page of Pentacles", 
    "Knight of Pentacles",
    "Queen of Pentacles", 
    "King of Pentacles",
]; 

const AGE: [&str; 3] = [
    "Past",
    "Present",
    "Future",
];

struct TarotCard {
    name: String,
    reversed: bool,
    age: String,
}

fn build_card(name: String, reversed: bool, age: String) -> TarotCard {
    TarotCard { name, reversed, age }
}

// counts specific patterns found in users tarot cards and prints meaning
fn interpret_patterns(cards: &Vec<TarotCard>){
    let mut count_rev = 0;
    let mut count_wnd = 0;
    let mut count_swd = 0;
    let mut count_pnt = 0;
    let mut count_cup = 0;
    let mut has_insight = false;
    for card in cards {
        if card.reversed {
            count_rev += 1;
            if count_rev > 1 {
                has_insight = true;
            }
        }
        if card.name.contains("Wands"){
            count_wnd += 1;
            if count_wnd > 1 {
                has_insight = true;
            }
        }
        if card.name.contains("Swords"){
            count_swd += 1;
            if count_swd > 1 {
                has_insight = true;
            }
        }
        if card.name.contains("Pentacles"){
            count_pnt += 1;
            if count_pnt > 1 {
                has_insight = true;
            }
        }
        if card.name.contains("Cups"){
            count_cup += 1;
            if count_cup > 1 {
                has_insight = true;
            }
        }
    }
    if has_insight {
        println!("Insight into your cards:");
    }
    if count_rev > 1 {
        println!("{} cards were reversed during this reading. Watch for blockages or delays.", count_rev);
    }
    if count_wnd > 1 {
        println!("Wand cards were a theme during your reading. This is a sign of strong energy, creativity, and action.");
    }
    if count_swd > 1 {
        println!("Sword cards were a theme during your reading. Mental clarity, conflict, or decision-making is highlighted.");
    }
    if count_pnt > 1 {
        println!("Pentacle cards were a theme during your reading. This is a sign of career, finance, or material stability.");
    }
    if count_cup > 1 {
        println!("Cup cards were a theme during your reading. Relationships, and intuition are prominent.");
    }
}

// looks up meaning of specified card in csv file
fn gather_meaning<P: AsRef<Path>>(tarot_file: P, card: &TarotCard) -> Result<(), Box<dyn Error>> {
    let tarot_file = File::open(tarot_file)?;
    let mut rdr = csv::Reader::from_reader(tarot_file);
    let card_name = format!("{}{}", card.name, if card.reversed{" Reversed"} else {""});
    for result in rdr.records() {
        let record = result?;   
        if record.get(0) == Some(&card_name) {
            if let Some(value) = record.get(1) {
                println!("Tarot Meaning: {}", value);
            }
        }
    }
    Ok(())
}

// randomly selects a tarot card that hasn't been picked yet this run
fn draw_card(drawn_cards: &[usize], age: &str) -> (TarotCard, usize) {
    let mut card_num = rand::rng().random_range(0..78);
    while drawn_cards.contains(&card_num) {
        card_num = rand::rng().random_range(0..78);
    }
    let is_reverse = rand::rng().random_range(0..2);
    let reversed = is_reverse == 1;
    (build_card(TAROT_CARDS[card_num].to_string(), reversed, age.to_string()), card_num)
}

fn main(){
    println!("here");
    let tarot_file = "tarot_cards.csv";
    let mut cards: Vec<TarotCard> = Vec::new();
    let mut drawn_cards = [0; 3];
    for i in 0..3 {
        let (card, tarot_index) = draw_card(&drawn_cards, AGE[i]);
        drawn_cards[i] = tarot_index;
        cards.push(card);
    }

    for card in &cards {
        let _ = gather_meaning(tarot_file, card);
    }
    println!("here");
    io::stdout().flush().unwrap();
}
