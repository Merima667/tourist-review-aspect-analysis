# Annotation Guidelines for the Bosnian Test Set

These guidelines describe how we annotate Bosnian reviews of Sarajevo restaurants and hotels.
They follow the SemEval-2016 Task 5 guidelines (Pontiki et al., 2016) and the category mapping in `data/README.md`, so that the Bosnian test set uses the same labels as the English and Turkish data.

## 1. Collecting reviews

- Collect public reviews of restaurants and hotels in Sarajevo, written in Bosnian (Croatian or Serbian spelling is also accepted).
- Before collecting, check the terms of use of the website. Record the website and the collection date.
- For each review, record whether it is about a **restaurant** or a **hotel** (`domain` column).
- Skip reviews that are not in Bosnian/Croatian/Serbian, are spam, or contain no opinion at all.

## 2. Anonymisation

Before a review is saved in the file:

- Never store the author's name, username, profile link or photo.
- Replace the names of people in the text (staff, the author, other guests) with `[NAME]`.
  Example: *"Konobar Amir je bio super."* → *"Konobar [NAME] je bio super."*
- Remove phone numbers, email addresses and links.
- Names of restaurants and hotels are kept, because the review texts are not published (see README, Bosnian test set).
 
## 3. Splitting into sentences

- One row in the CSV file is one sentence.
- Split at `.`, `!` and `?`. Do not split at commas.
- Keep the original text: do not correct spelling, add diacritics or change words (except for anonymisation).
- `review_id`: `bs001`, `bs002`, ... ; `sentence_id`: `bs001:0`, `bs001:1`, ...

## 4. Aspects

Each sentence gets a label for each of four aspects:

| Aspect | Restaurant | Hotel |
|---|---|---|
| **food** | quality, taste, choice and portions of food and drinks | breakfast, hotel restaurant, bar, drinks |
| **staff** | waiters, service, speed of service, friendliness | reception, housekeeping, waiters, any hotel staff |
| **price** | prices of food and drinks, value for money | room price, breakfast price, value for money |
| **location** | where the place is, access, surroundings, view | where the hotel is, distance to the centre, surroundings, view |

**Ignored** (labelled `none` in all four columns, unless the sentence also mentions one of the four aspects):

- ambience, music, decoration, noise
- general opinions about the place (*"Super mjesto."*, *"Preporučujem!"*)
- hotel rooms, beds, bathrooms, cleanliness, Wi-Fi, parking, facilities

## 5. Labels

| Label | When to use it | Example |
|---|---|---|
| `positive` | the aspect is praised | *"Ćevapi su bili odlični."* → food |
| `negative` | the aspect is criticised | *"Konobar je bio neljubazan."* → staff |
| `neutral` | an opinion without a clear positive or negative direction | *"Hrana je bila OK, ništa posebno."* → food |
| `conflict` | the same aspect is both praised and criticised in the same sentence | *"Predjelo je bilo odlično, ali pivo toplo."* → food |
| `none` | the aspect is not mentioned, or it is mentioned without any opinion | *"Naručili smo pizzu."* → food = none |

Labels are written exactly like this, in lowercase.

## 6. Rules

1. **Prices go to price, not food.** *"Ćevapi su preskupi."* → food = none, price = negative.
2. **Drinks go to food.** *"Kafa je odlična."* → food = positive.
3. **Implicit opinions count.** *"Čekali smo hranu 45 minuta."* → staff = negative (slow service).
4. **Only the reviewed place counts.** Opinions about other restaurants or hotels are ignored.
5. **One sentence can have several aspects.** *"Ćevapi su bili odlični, ali konobar je bio neljubazan."* → food = positive, staff = negative.
6. **Value for money goes to price.** *"Za te pare vrijedi."* → price = positive.
7. **Irony and sarcasm:** label the intended meaning. *"Baš brza usluga, samo sat vremena čekanja."* → staff = negative.
8. **When in doubt**, write the sentence ID in a list of unclear cases and discuss it with the team. Do not guess.

## 7. Example rows

```
review_id,sentence_id,language,domain,text,food,staff,price,location
bs001,bs001:0,bs,restaurant,"Ćevapi su bili odlični, ali konobar je bio neljubazan.",positive,negative,none,none
bs001,bs001:1,bs,restaurant,"Cijene su malo visoke za ovaj dio grada.",none,none,negative,none
bs002,bs002:0,bs,hotel,"Hotel je odmah pored Baščaršije.",none,none,none,positive
bs002,bs002:1,bs,hotel,"Soba je bila čista i prostrana.",none,none,none,none
bs002,bs002:2,bs,hotel,"Doručak je bio bogat, a osoblje na recepciji ljubazno.",positive,positive,none,none
```

## 8. Inter-annotator agreement

- Two team members annotate the same 50 randomly selected reviews (25 restaurant and 25 hotel reviews) **independently**, each in her own file, without AI tools and without discussing the labels.
- Cohen's kappa is computed per aspect.
- Disagreements are then discussed, and the final label is written in `data/processed/bs_test.csv`.

## 9. File format

- File: `data/processed/bs_test.csv`
- Encoding: UTF-8 (in Excel: *Save As → CSV UTF-8*), so that č, ć, š, ž and đ are kept.

## 10. Rules added during annotation

These rules were agreed on during annotation of the Bosnian test set:

1. **Each sentence is labelled on its own.** The rest of the review is used only to understand what a sentence refers to (e.g. who "he" is), not to add an opinion that is not in the sentence.
2. **Speed of service is staff.** "Hrana bude brzo gotova." → staff = positive.
3. **State of a room vs. service.** A sentence that only describes the state of a room is ignored ("Soba je bila prljava." → none). A sentence that describes a service that was not done is staff ("Ručnici nisu mijenjani 4 dana." → staff = negative).
4. **"ok", "u redu", "osrednje", "prosječno" are neutral.**
5. **"Lokacija" meaning "a place to visit" is a general opinion.** "Jedna od top lokacija za posjetiti." → none. Location is only where the place is: distance to the centre, surroundings, transport, view.
6. **Parking is ignored**, like other facilities.
7. **Value for money is price**, also when it is said through portions: "Puno dođe hrane, opravdava cijenu." → price = positive, food = positive.
