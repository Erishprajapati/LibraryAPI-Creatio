from database import SessionLocal
from models import Book

def add_books():
    db = SessionLocal()
    
    books_data = [
        {"title": "To Kill a Mockingbird", "description": "A powerful story of racial injustice and the loss of innocence in the American South, following a young girl whose father defends a Black man falsely accused of a serious crime.", "author": "Harper Lee", "published_date": 1960},
        {"title": "1984", "description": "A dystopian social science fiction novel that follows the life of Winston Smith, a low-ranking member of 'the Party', who is frustrated by the omnipresent eyes of the party watching him.", "author": "George Orwell", "published_date": 1949},
        {"title": "The Great Gatsby", "description": "A story of the fabulously wealthy Jay Gatsby and his love for the beautiful Daisy Buchanan, an exploration of the American Dream and the Jazz Age.", "author": "F. Scott Fitzgerald", "published_date": 1925},
        {"title": "Pride and Prejudice", "description": "A romantic novel of manners that follows the emotional development of Elizabeth Bennet, who learns about the repercussions of hasty judgments and comes to appreciate the difference between superficial goodness and actual goodness.", "author": "Jane Austen", "published_date": 1813},
        {"title": "The Hobbit", "description": "A fantasy novel about Bilbo Baggins, a hobbit who embarks on a quest to reclaim the Lonely Mountain from the dragon Smaug.", "author": "J.R.R. Tolkien", "published_date": 1937},
        {"title": "The Catcher in the Rye", "description": "A novel about teenage alienation and loss of innocence in which Holden Caulfield struggles with the phoniness of the adult world.", "author": "J.D. Salinger", "published_date": 1951},
        {"title": "Lord of the Flies", "description": "A novel about a group of British boys stranded on an uninhabited island and their disastrous attempts to govern themselves. It explores the dark side of human nature.", "author": "William Golding", "published_date": 1954},
        {"title": "Animal Farm", "description": "An allegorical novella about a group of farm animals who rebel against their human farmer, hoping to create a society where the animals can be equal, free, and happy.", "author": "George Orwell", "published_date": 1945},
        {"title": "The Lord of the Rings", "description": "An epic high-fantasy novel about the quest to destroy a powerful ring, following Frodo Baggins and the Fellowship of the Ring.", "author": "J.R.R. Tolkien", "published_date": 1954},
        {"title": "Jane Eyre", "description": "A novel about a young orphan who becomes a governess and falls in love with her employer, exploring themes of love, independence, and social class.", "author": "Charlotte Brontë", "published_date": 1847},
        {"title": "Wuthering Heights", "description": "A gothic novel about the intense and passionate love between Catherine Earnshaw and Heathcliff, and how their love affects the lives of those around them.", "author": "Emily Brontë", "published_date": 1847},
        {"title": "Moby-Dick", "description": "An epic tale of Captain Ahab's obsessive quest to hunt down Moby Dick, the white whale that had previously destroyed his ship and severed his leg.", "author": "Herman Melville", "published_date": 1851},
        {"title": "The Adventures of Huckleberry Finn", "description": "A novel about Huck Finn's journey down the Mississippi River with a runaway slave, exploring themes of race, freedom, and American society.", "author": "Mark Twain", "published_date": 1884},
        {"title": "The Scarlet Letter", "description": "A novel about Hester Prynne, who is forced to wear a scarlet letter 'A' as punishment for adultery. It explores themes of sin, guilt, and redemption.", "author": "Nathaniel Hawthorne", "published_date": 1850},
        {"title": "Don Quixote", "description": "A novel about Alonso Quixano, a nobleman who becomes so obsessed with chivalric romances that he decides to become a knight-errant himself.", "author": "Miguel de Cervantes", "published_date": 1605},
        {"title": "The Divine Comedy", "description": "An epic poem that describes Dante's journey through Hell, Purgatory, and Paradise, considered one of the greatest works of world literature.", "author": "Dante Alighieri", "published_date": 1320},
        {"title": "Hamlet", "description": "A tragedy about Prince Hamlet of Denmark, who seeks revenge against his uncle for murdering his father and marrying his mother.", "author": "William Shakespeare", "published_date": 1603},
        {"title": "Romeo and Juliet", "description": "A tragedy about two young lovers from feuding families whose deaths ultimately reconcile their families.", "author": "William Shakespeare", "published_date": 1597},
        {"title": "Macbeth", "description": "A tragedy about Macbeth, a Scottish general who receives a prophecy that he will become King of Scotland, and the consequences of his ambition.", "author": "William Shakespeare", "published_date": 1623},
        {"title": "The Odyssey", "description": "An epic poem about Odysseus's ten-year journey home from the Trojan War, facing numerous obstacles and adventures along the way.", "author": "Homer", "published_date": -800},
        {"title": "The Iliad", "description": "An epic poem about the Trojan War, focusing on the quarrel between King Agamemnon and the warrior Achilles.", "author": "Homer", "published_date": -750},
        {"title": "The Brothers Karamazov", "description": "A philosophical novel about the murder of Fyodor Karamazov and the impact on his sons, exploring themes of faith, doubt, and morality.", "author": "Fyodor Dostoevsky", "published_date": 1880},
        {"title": "Crime and Punishment", "description": "A novel about Rodion Raskolnikov, a poor ex-student who commits murder and the psychological consequences he faces.", "author": "Fyodor Dostoevsky", "published_date": 1866},
        {"title": "War and Peace", "description": "A novel that follows five aristocratic families during the Napoleonic Wars, exploring themes of love, war, and the meaning of life.", "author": "Leo Tolstoy", "published_date": 1869},
        {"title": "Anna Karenina", "description": "A novel about Anna Karenina, a married woman who has an affair with Count Vronsky, and the consequences of her actions.", "author": "Leo Tolstoy", "published_date": 1877},
        {"title": "Les Misérables", "description": "A novel about Jean Valjean, a former convict who seeks redemption, and his interactions with various characters in 19th-century France.", "author": "Victor Hugo", "published_date": 1862},
        {"title": "The Hunchback of Notre-Dame", "description": "A novel about Quasimodo, a deformed bell-ringer of Notre-Dame Cathedral, and his love for the beautiful Esmeralda.", "author": "Victor Hugo", "published_date": 1831},
        {"title": "Madame Bovary", "description": "A novel about Emma Bovary, a doctor's wife who seeks escape from her mundane life through romantic affairs and material possessions.", "author": "Gustave Flaubert", "published_date": 1857},
        {"title": "The Count of Monte Cristo", "description": "A novel about Edmond Dantès, who is wrongfully imprisoned and seeks revenge against those who betrayed him.", "author": "Alexandre Dumas", "published_date": 1844},
        {"title": "The Three Musketeers", "description": "A novel about d'Artagnan, a young man who joins the Musketeers of the Guard and becomes involved in political intrigue.", "author": "Alexandre Dumas", "published_date": 1844},
        {"title": "The Picture of Dorian Gray", "description": "A novel about Dorian Gray, a beautiful young man whose portrait ages while he remains young, exploring themes of beauty, morality, and corruption.", "author": "Oscar Wilde", "published_date": 1890},
        {"title": "Dracula", "description": "A gothic horror novel about Count Dracula's attempt to move from Transylvania to England to spread the undead curse.", "author": "Bram Stoker", "published_date": 1897},
        {"title": "Frankenstein", "description": "A novel about Victor Frankenstein, a scientist who creates a sapient creature in an unorthodox scientific experiment.", "author": "Mary Shelley", "published_date": 1818},
        {"title": "The Strange Case of Dr Jekyll and Mr Hyde", "description": "A novel about Dr. Henry Jekyll, who creates a potion that transforms him into the evil Mr. Edward Hyde.", "author": "Robert Louis Stevenson", "published_date": 1886},
        {"title": "Treasure Island", "description": "A novel about young Jim Hawkins, who finds a map to buried treasure and sets sail with pirates to find it.", "author": "Robert Louis Stevenson", "published_date": 1883},
        {"title": "Alice's Adventures in Wonderland", "description": "A novel about Alice, who falls down a rabbit hole into a fantasy world populated by peculiar creatures.", "author": "Lewis Carroll", "published_date": 1865},
        {"title": "Through the Looking-Glass", "description": "A sequel to Alice's Adventures in Wonderland, where Alice enters a fantastical world through a mirror.", "author": "Lewis Carroll", "published_date": 1871},
        {"title": "The Time Machine", "description": "A science fiction novel about a time traveler who journeys to the year 802,701 and discovers the future of humanity.", "author": "H.G. Wells", "published_date": 1895},
        {"title": "The War of the Worlds", "description": "A science fiction novel about an invasion of Earth by Martians, told from the perspective of an unnamed narrator.", "author": "H.G. Wells", "published_date": 1898},
        {"title": "The Invisible Man", "description": "A science fiction novel about Griffin, a scientist who makes himself invisible but cannot reverse the process.", "author": "H.G. Wells", "published_date": 1897},
        {"title": "The Call of the Wild", "description": "A novel about Buck, a domesticated dog who is stolen and sold into service as a sled dog in Alaska.", "author": "Jack London", "published_date": 1903},
        {"title": "White Fang", "description": "A novel about White Fang, a wolf-dog hybrid who is raised in the wild but eventually becomes domesticated.", "author": "Jack London", "published_date": 1906},
        {"title": "The Jungle", "description": "A novel about Jurgis Rudkus, a Lithuanian immigrant who experiences the harsh realities of industrial capitalism.", "author": "Upton Sinclair", "published_date": 1906},
        {"title": "The Metamorphosis", "description": "A novella about Gregor Samsa, a traveling salesman who wakes up one morning to find himself transformed into a giant insect.", "author": "Franz Kafka", "published_date": 1915},
        {"title": "The Trial", "description": "A novel about Josef K., a man who is arrested and prosecuted by a remote, inaccessible authority, with the nature of his crime revealed neither to him nor to the reader.", "author": "Franz Kafka", "published_date": 1925},
        {"title": "Ulysses", "description": "A modernist novel that follows Leopold Bloom through Dublin during an ordinary day, using stream-of-consciousness technique.", "author": "James Joyce", "published_date": 1922},
        {"title": "A Portrait of the Artist as a Young Man", "description": "A novel about Stephen Dedalus, a young man who grows up in Ireland and struggles with questions of identity, religion, and art.", "author": "James Joyce", "published_date": 1916},
        {"title": "The Sound and the Fury", "description": "A novel about the Compson family, told from four different perspectives, exploring themes of time, memory, and the decline of the American South.", "author": "William Faulkner", "published_date": 1929},
        {"title": "As I Lay Dying", "description": "A novel about the Bundren family's journey to bury their mother Addie, told from multiple perspectives.", "author": "William Faulkner", "published_date": 1930},
        {"title": "The Grapes of Wrath", "description": "A novel about the Joad family, who are forced to leave their farm during the Great Depression and travel to California in search of work.", "author": "John Steinbeck", "published_date": 1939},
        {"title": "Of Mice and Men", "description": "A novella about George Milton and Lennie Small, two displaced migrant ranch workers who move from place to place in California during the Great Depression.", "author": "John Steinbeck", "published_date": 1937},
        {"title": "East of Eden", "description": "A novel about two families, the Trasks and the Hamiltons, whose generations parallel the biblical story of Cain and Abel.", "author": "John Steinbeck", "published_date": 1952},
        {"title": "The Old Man and the Sea", "description": "A novel about Santiago, an aging Cuban fisherman who struggles with a giant marlin far out in the Gulf Stream.", "author": "Ernest Hemingway", "published_date": 1952},
        {"title": "For Whom the Bell Tolls", "description": "A novel about Robert Jordan, an American volunteer in the International Brigades during the Spanish Civil War.", "author": "Ernest Hemingway", "published_date": 1940},
        {"title": "A Farewell to Arms", "description": "A novel about Frederic Henry, an American ambulance driver in the Italian army during World War I.", "author": "Ernest Hemingway", "published_date": 1929},
        {"title": "The Sun Also Rises", "description": "A novel about a group of American and British expatriates who travel from Paris to Pamplona to watch the running of the bulls.", "author": "Ernest Hemingway", "published_date": 1926},
        {"title": "One Hundred Years of Solitude", "description": "A novel about the Buendía family over seven generations, exploring themes of time, memory, and Latin American history.", "author": "Gabriel García Márquez", "published_date": 1967},
        {"title": "Love in the Time of Cholera", "description": "A novel about Florentino Ariza and Fermina Daza, whose love story spans more than fifty years.", "author": "Gabriel García Márquez", "published_date": 1985},
        {"title": "The Alchemist", "description": "A novel about Santiago, a young Andalusian shepherd who dreams of finding a worldly treasure and embarks on a journey to find it.", "author": "Paulo Coelho", "published_date": 1988},
        {"title": "The Kite Runner", "description": "A novel about Amir, a young boy from Kabul, and his journey of redemption after betraying his best friend Hassan.", "author": "Khaled Hosseini", "published_date": 2003},
        {"title": "A Thousand Splendid Suns", "description": "A novel about two women, Mariam and Laila, whose lives become intertwined in war-torn Afghanistan.", "author": "Khaled Hosseini", "published_date": 2007}
    ]
    
    for book_data in books_data:
        book = Book(**book_data)
        db.add(book)
    
    db.commit()
    print(f"Added {len(books_data)} books to the database!")
    db.close()

if __name__ == "__main__":
    add_books() 