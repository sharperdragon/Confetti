Confetti Reinforcement Add-on for Anki
======================================

Overview
--------
The Confetti Reinforcement Add-on adds a fun visual boost to your Anki review sessions by displaying 
a burst of confetti when specific conditions based on your card’s performance are met. It is designed 
to integrate with FSRS (Free Spaced Repetition Scheduler) by allowing you to trigger confetti based on 
searchable card properties such as retrievability, difficulty, stability, overdue interval, ease, reps, 
retention, and more.

Key Features:
  • Configurable confetti effects: Adjust particle count, spread, speed, duration, and fade.
  • Condition-based triggers: Fire confetti when custom conditions (e.g., “prop:r < 0.40 AND prop:reps >= 3”)
    are met.
  • FSRS Integration: Use the same searchable card properties as you would in the Anki browser.
  • Global rating check: Confetti only fires if the card is rated “good” (ease = 3) or “easy” (ease = 4).
  • Detailed in-app configuration guide.

Installation
------------
1. Prepare the Add-on Folder:
   - Ensure your add-on folder (e.g., “confetti”) contains at least these files:
       • __init__.py
       • config.json
   - (Optional) Include additional files such as images, sound files, or a README if desired.

2. Place the Folder in Your Add-ons Directory:
   - On macOS: Place the folder in 
         ~/Library/Application Support/Anki2/addons21/
   - On Windows: Place the folder in 
         C:\Users\<YourName>\AppData\Roaming\Anki2\addons21\

3. Restart Anki:
   - Close and reopen Anki to load the add-on. Verify that it appears in the Add-ons dialog.

Usage
-----
- Once installed, the add-on automatically monitors your review sessions.
- Confetti will be triggered only when:
    a) The card is rated "good" (ease = 3) or "easy" (ease = 4).
    b) One of the defined trigger conditions is met. For example:
       - If the card's retrievability (prop:r) is below 0.40 and it has been reviewed at least 3 times 
         (prop:reps >= 3).
       - If the card is in review (is:review) and its difficulty (prop:d) is at least 0.90.
       - If three consecutive reviews were rated “again” (last_n_again = 3).
       - If the card is overdue (prop:due < -24) and there are no recent “again” responses (last_n_again = 0).
       - If, in the last 4 reviews, the card was rated either “again” or “hard” 
         (last_n_again|hard = 4).
- You can modify these conditions and the visual effect parameters via the config.json file.

Configuration
-------------
The main configuration file, config.json, is located in your add-on folder. Key sections include:

Global Options:
  - default_origins: Defines the screen coordinates for co
