import os
import random

# --- משתנים גלובליים קבועים כפי שנדרש ---
MAX_TRIES = 6  # מקסימום ניסיונות כושלים מותרים [cite: 20]

# מילון המייצג את מצבי האיש התלוי בכל אחד מהמצבים [cite: 22]
HANGMAN_PHOTOS = {
    0: """
    x-------x
    """,
    1: """
    x-------x
    |
    |
    |
    |
    |
    """,
    2: """
    x-------x
    |       |
    |       0
    |
    |
    |
    """,
    3: """
    x-------x
    |       |
    |       0
    |      /|\\
    |
    |
    """,
    4: """
    x-------x
    |       |
    |       0
    |      /|\\
    |      /
    |
    """,
    5: """
    x-------x
    |       |
    |       0
    |      /|\\
    |      / \\
    |
    """,
    6: """
    x-------x
    |       |
    |       0
    |      /|\\
    |      / \\
    |
    """
}

# --- פונקציות עזר (כפי שנדרש - משימות מתגלגלות) ---

# פונקציה להצגת מסך הפתיחה (נדרש לאגד בפונקציה מסודרת) [cite: 13, 26]
def print_start_screen():
    """מדפיסה את מסך הפתיחה של המשחק עם האיור המעוצב."""
    HANGMAN_ART = """
    _ _ _ _ _ _
    | | | | | |
    | _ _ | | _ _ | | _ _ | | _ _ | | _ _ |
    | _ _ / | _ _ / | _ _ / | _ _ / | _ _ / |
    | | | ( _ | | | ( _ | | | ( _ | | | ( _ |
    | | | \ _ _ , | _ _ , | \ _ _ , | _ _ , |
    | _ _ /
    | _ _ _ /
    """
    # הדפסת מסך הפתיחה כפי שמופיע בדוגמאות הפלט
    print("# Print the Welcome Screen")
    print(HANGMAN_ART)
    print(f"MAX TRIES: {MAX_TRIES}")
    print("Let’s start!")

# 1. פונקציית check_win [cite: 4, 48]
def check_win(secret_word, old_letters_guessed):
    """
    פונקציה בוליאנית המחזירה אמת אם כל אות במילה הסודית (secret_word)
    נכללת ברשימת האותיות שניחש השחקן (old_letters_guessed). אחרת, מחזירה שקר[cite: 4, 5].
    """
    for letter in secret_word:
        if letter not in old_letters_guessed:
            return False
    return True

# 2. פונקציית show_hidden_word [cite: 6, 49]
def show_hidden_word(secret_word, old_letters_guessed):
    """
    מחזירה מחרוזת המורכבת מאותיות ומקווים תחתונים[cite: 6].
    המחרוזת מציגה את האותיות מתוך old_letters_guessed שנמצאות ב-secret_word במיקומן
    המתאים, ואת שאר האותיות כקווים תחתונים[cite: 7].
    """
    result = ""
    for letter in secret_word:
        if letter in old_letters_guessed:
            result += letter + " "
        else:
            result += "_ "
    return result.strip()

# 3. פונקציית check_valid_input [cite: 8, 50]
def check_valid_input(letter_guessed, old_letters_guessed):
    """
    בודקת את תקינות הקלט ואת חוקיות הניחוש (טרם ניחשו אות זו) ומחזירה אמת או שקר בהתאם[cite: 9].
    """
    letter_guessed = letter_guessed.lower()
    
    # בדיקת אורך התו
    if len(letter_guessed) != 1:
        return False
    
    # בדיקה האם התו הוא אות אנגלית
    if not 'a' <= letter_guessed <= 'z':
        return False
    
    # בדיקה האם האות נוחשה כבר בעבר
    if letter_guessed in old_letters_guessed:
        return False
        
    return True

# 4. פונקציית try_update_letter_guessed [cite: 10, 51]
def try_update_letter_guessed(letter_guessed, old_letters_guessed):
    """
    משתמשת ב-check_valid_input לבדיקת תקינות.
    אם התו תקין ולא ניחשו אותו בעבר - הפונקציה מוסיפה את התו לרשימת הניחושים ומחזירה אמת[cite: 11].
    אחרת - מדפיסה 'X', את רשימת האותיות שכבר נוחשו ומחזירה שקר[cite: 10].
    """
    letter_guessed = letter_guessed.lower()
    
    if check_valid_input(letter_guessed, old_letters_guessed):
        # הקלט תקין - מוסיפים לרשימה
        old_letters_guessed.append(letter_guessed)
        return True
    else:
        # הקלט אינו תקין או שכבר נוחש
        print("X")
        # מיון והדפסת רשימת האותיות שכבר נוחשו (כמחרוזת, מופרדת בחצים)
        sorted_letters = sorted([l.lower() for l in old_letters_guessed])
        print(" -> ".join(sorted_letters))
        return False

# 5. פונקציית choose_word [cite: 12, 52]
def choose_word(file_path, index):
    """
    מקבלת נתיב לקובץ ואינדקס ומחזירה את המילה הסודית במיקום index[cite: 12].
    """
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None

    # מפרידים את המילים ומסירים כפילויות כדי לקבל מילים ייחודיות
    words = content.split()
    unique_words = sorted(list(set(words))) # מיון לצורך עקביות

    # טיפול באינדקס לא תקין
    if index <= 0 or index > len(unique_words):
        print(f"Error: Index {index} is out of bounds. The file has {len(unique_words)} unique words.")
        return None

    # חישוב המיקום בפייתון (אינדקס מינוס 1)
    # שימוש באופרטור מודולו כדי להתמודד עם אינדקסים גדולים מדי אם תרצה שהרשימה "תתעטף"
    word_index = (index - 1) % len(unique_words) 
    
    # החזרת המילה במיקום
    return unique_words[word_index].lower()


# --- פונקציית המשחק המרכזית (hangman) ---

def hangman(secret_word):
    """
    פונקציית המשחק המרכזית. מנהלת את לוגיקת משחק איש תלוי.
    """
    # משתנים נדרשים
    old_letters_guessed = []  # הרשימה מחזיקה את האותיות שהשחקן ניחש עד כה [cite: 19]
    num_of_tries = 0          # מספר הניסיונות הכושלים של המשתמש עד כה [cite: 21]

    # הצגת מצב האיש התלוי הראשוני (0 ניסיונות) [cite: 29]
    print(HANGMAN_PHOTOS[num_of_tries])
    
    # הצגת המילה הסודית כקווים תחתונים [cite: 30]
    print(show_hidden_word(secret_word, old_letters_guessed))

    # לולאת המשחק הראשית (כל עוד לא ניצחנו ולא נגמרו הניסיונות)
    while num_of_tries < MAX_TRIES and not check_win(secret_word, old_letters_guessed):
        
        # קבלת קלט מהשחקן
        letter_guessed = input("Guess a letter: ")
        
        # ניסיון לעדכן את רשימת הניחושים
        if try_update_letter_guessed(letter_guessed, old_letters_guessed):
            # הקלט תקין - נבדוק האם הניחוש נכון
            
            if letter_guessed.lower() in secret_word:
                # ניחוש מוצלח - רק מציגים את המצב המעודכן
                print(show_hidden_word(secret_word, old_letters_guessed))
            else:
                # ניחוש כושל - עדכון ניסיונות והצגת הפסד + תמונה [cite: 32]
                num_of_tries += 1
                print(":(")
                print(HANGMAN_PHOTOS[num_of_tries]) # הצגת מצב מתקדם יותר [cite: 32]
                print(show_hidden_word(secret_word, old_letters_guessed))

    # סיום המשחק
    if check_win(secret_word, old_letters_guessed):
        # ניצחון [cite: 34]
        print("WIN")
    else:
        # הפסד [cite: 35]
        print("LOSE")

# --- פונקציה ראשית (main) ---

def main():
    """
    הפונקציה הראשית של התוכנית. מנהלת את לולאת ההפעלה החוזרת של המשחק.
    """
    play_again = True
    
    # לולאה המאפשרת למשתמש לשחק שוב ושוב [דרישה חדשה]
    while play_again:
        
        # 1. הדפסת מסך הפתיחה
        print_start_screen() 
        
        secret_word = None
        # לולאה לקבלת קלט תקין של קובץ ואינדקס
        while secret_word is None:
            file_path = input("Enter file path: ")
            try:
                # קליטת האינדקס
                index_str = input("Enter index: ")
                index = int(index_str)
            except ValueError:
                # טיפול במקרה של קלט שאינו מספר עבור האינדקס
                print("Invalid index. Must be a whole number.")
                continue

            # בחירת המילה הסודית
            secret_word = choose_word(file_path, index)
            
        # התחלת המשחק
        hangman(secret_word)
        
        # שאלה האם לשחק שוב
        while True:
            choice = input("Would you like to play again? (y/n): ").lower()
            if choice == 'y':
                play_again = True
                break
            elif choice == 'n':
                play_again = False
                break
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

# תנאי להרצת הפונקציה הראשית [cite: 53]
if __name__ == "__main__":
    main()