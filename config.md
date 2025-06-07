
### Confetti Celebration! 

<div style="color:rgb(57, 91, 149); font-weight: bold;">Please note that you will have to restart Anki for some of these options to apply (e.g., modifying default confetti parameters or toggling success sound).</div>

- <b><u>play_success_sound `[true/false]`</u></b>: enables or disables a success sound when confetti is triggered; default: `true`
- <b><u>success_sound `[string]`</u></b>: absolute path to the sound file played when confetti triggers; default: `"/absolute/path/to/your/success_sound.wav"`
- <b><u>particleCount `[integer]`</u></b>: number of confetti particles; default: `150`
- <b><u>spread `[integer]`</u></b>: spread angle of confetti; default: `100`
- <b><u>speed `[integer]`</u></b>: initial velocity of confetti; default: `45`
- <b><u>duration `[integer]`</u></b>: duration in milliseconds; default: `200`
- <b><u>decay `[float]`</u></b>: confetti fade-out factor (lower values decay faster, lower power confetti); default: `0.9`
- <b><u>opacity `[float]`</u></b>: transparency of confetti particles (0.0 = fully transparent, 1.0 = fully opaque); default: `1.0`
- <b><u>origins `[array]`</u></b>: screen coordinates where confetti originates; default: `[{ "x": 0.1, "y": 1.0 }, { "x": 0.9, "y": 1.0 }]`

<h1>Conditions</h1>
- *<b><u>prop:r  `[float]`</u></b>*: **Retrievability** of the card (probability of successful recall)<br><u>example</u>: `prop:r < 0.40`
- *<b><u>prop:reps  `[integer]`</u></b>*: **Number of times the card has been reviewed<br><u>example</u>: `prop:reps >= 3`
- *<b><u>prop:due ` [integer]`</u></b>*: **How overdue the card is (negative = overdue)<br><u>example</u>: `prop:due < -15`
- *<b><u>prop:ease  `[float]`</u></b>*: **Ease factor is low (indicating a difficult card)<br><u>example</u>: `prop:ease < 2.5`
- *<b><u>is:review  `[true/false]`</u></b>*: **Indicates if the card is in review phase<br><u>example</u>: `is:review = true`
- *<b><u>prop:reps  `[integer]`</u></b>*: **Card has been reviewed <i>at least</i> 10 times<br><u>example</u>: `prop:reps > 10`
<br>
- *<b><u>last_n_again `[integer]`</u></b>*: **Number of consecutive times the card was rated "again"<br><u>example</u>: `last_n_again = 3`
<br>
- *<b><u>prop:d  `[0-10]`</u></b>*: **Difficulty** of the card. 1 being easy, 10 being most difficult<br><u>example</u>: `prop:d >= 9.4`
- *<b><u>prop:s  `[0+]`</u></b>*: **Stability** of the card (higher means more stable memory), measured in days<br><u>example</u>: `prop:s <= 5.0`
- *<b><u>prop:r  `[0-1.0]`</u></b>*: **Probability of recalling the card correctly.<br><u>example</u>: `prop:r <= 0.30`




- <b><u>fsrs_properties `[dict]`</u></b>: mapping of FSRS card properties for trigger conditions; default:
  ```json
  {
    "difficulty": "d",
    "retrievability": "r",
    "stability": "s"
  }
  ```

