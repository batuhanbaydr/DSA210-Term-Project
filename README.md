# Project Name: Are the Oscars going "Woke"?

## Terminology:

- Woke: Aware of and actively attentive to important societal facts and issues (especially issues of racial and social justice)
- Bechdel Test: Is a measure of the representation of women in film and other fiction. The test asks whether a work features at least two women who have a conversation about something other than a man.

## Description
In recent years, debates surrounding diversity and political influence in the Academy Awards have intensified. These discussions reached a peak during the 97th Academy Awards, when a movie named "Emilia Pérez" received 13 nominations, despite widespread public criticism and accusations of an unfair selection process. Many viewers argued that its nominations were driven by political considerations rather than artistic merit.

With this project, as a follower of the Academy Awards, I aim to analyze whether the Oscars have become increasingly politically motivated by examining long-term trends in the race, gender, and thematic political content of nominees and winners. Through data-driven analysis, I will investigate whether the Oscars have shifted toward favoring politically charged films over cinematic criteria.

## Project Goal
The project aims to answer these questions
- Has there been a shift in the racial composition of nominees and winners?
- Do movies passing the Bechdel Test win more often?
- Are movies with political/social themes have higher winning rates?

## Dataset Description
- [Academy awards dataset (oscars) by DHARMIK DONGA on Kaggle](https://www.kaggle.com/datasets/dharmikdonga/academy-awards-dataset-oscars/data): : Will be used for races of the nominees and winners.
- [TMDB API](https://developer.themoviedb.org/docs/getting-started): Will be used for getting the keywords(themes) of the movies.
- [Bechdel Test Data](https://bechdeltest.com): Will be used to see whether the film passes the test or not.

I will be filtering out the data from TMDB API and Bechdel Test Datasets to use only Oscar nominated movies.

## For 25 April: EDA & Hypothesis Tests

*Dataset:* `oscars_plus_bechdel_pol.parquet`  
Rows = 10 856 Bechdel matches = 5 810 Political films = 614

### Key χ² Results

| Test | χ² | p‑value | Interpretation |
|------|----|---------|----------------|
| Bechdel pass × Winner | **0.74** | 0.391 | Not significant – Bechdel pass does not affect winning |
| Political theme × Winner | **13.12** | 0.00029 | Significant – political films win more often |
| Racial shift Nominees (pre‑2000 vs 2000+) | **235.16** | 1.06 × 10⁻⁵⁰ | Significant – nominee racial mix changed |
| Racial shift Winners (pre‑2000 vs 2000+) | **107.99** | 2.97 × 10⁻²³ | Significant – winner racial mix changed |

### Visual Insights
* Nominee counts fairly stable per decade; big spike 1940s.  
* Bechdel pass fraction rises steadily since 1970s.  
* Political‐theme nominations appear mainly after 2000.  
* Win rate ~22 % overall; rises to ~28 % for political films.

**Sources:** Kaggle Academy Awards XLSX · BechdelTest API v1 · TMDB API (keywords + genres)  
