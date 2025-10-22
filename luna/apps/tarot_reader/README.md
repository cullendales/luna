# Arcana

<img width="649" height="510" alt="Screenshot 2025-10-16 at 3 55 34 PM" src="https://github.com/user-attachments/assets/7fe69a61-fddb-4a57-b773-30dba8773419" />


## About
Arcana displays tarot cards representing your past, present, and future, along with their meanings. Your fortune awaits.

## Usage

### Requirements
- Arcana requires a terminal that can display coloured images such as iTerm or Kitty. The program will work without printing an image otherwise which is fine but loses some of the fun.
- Rust must be installed.

### Set Up
1. Clone Repo
```
git clone https://github.com/cullendales/arcana
```
2. Navigate inside repo root and run program to learn about yourself!
```
cargo run
```

## Notes
Each card has its meaning displayed individually, with the program only giving some insights about all 3 cards together. Actually interpreting meanings of all 3 cards put together would require an extensive csv file as there are 3,651,648 possible combinations! I'm not going to write that many interpretations, are you? Anyways, interpretations are not a defined result and are up to the reader as they are with regular tarot cards.

This is my first Rust project, so please don't judge my code too much if it is unoptimized in some parts. Enjoy finding out your fortune!
