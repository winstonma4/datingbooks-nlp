# datingbooks-nlp
The purpose of this project was to use natural language processing in order to analyze whether men and women think differently about dating and relationships. 74 books were scraped, cleaned, and split into documents of 20 sentences each before being vectorized using a TF-IDF vectorizer. These document vectors were then processed using a non-negative matrix factorization model in order to arrive at 18 different topics. A flask app was also built in order to recommend books to users who are interested in further discovering specific topics. The recommendation results show how close of a match each book is to the user's selected topics and directs the user to Amazon to then purchase the book. 

Takeaways from this project:

  1. While male and female authors on the subject both discuss similar topics, males tend to focus on the science of attraction and associated techniques, while women are more willing to discuss the causes of heartbreak
  2. Both male and female authors prioritize the idea of embracing "being alpha" and/or developing the self-confidence to get there in order to improve the quality of both people's lives in a relationship
  3. The topic of family tends to have more negative sentiment, as both male and female authors discuss unattractive behaviors as a result of subconscious influence from our upbringing

Future discovery:

  1. Apply this to texts of different cultures and languages
  2. Gain access to dating app data to see whether these "dating experts'" ideas apply
