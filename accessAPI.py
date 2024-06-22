# Constants
BASE_URL = "https://openscriptureapi.org/api/scriptures/v1/lds/en/volume/bookofmormon/"
BOOKS_URL = "https://openscriptureapi.org/api/scriptures/v1/lds/en/volume/bookofmormon/_index"

def get_books():
    try:
        response = requests.get(BOOKS_URL)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        return data["books"]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching books data from the API: {str(e)}")
        return []

def main():
    print("Welcome to the Book of Mormon Summary Tool!")
    
    books = get_books()
    if not books:
        print("Failed to fetch the list of books. Exiting.")
        return
    
    # Print available books
    print("Available Books:")
    for idx, book in enumerate(books, start=1):
        print(f"{idx}. {book['title']}")
    
    while True:
        try:
            # Ask user for book choice
            choice = int(input("Enter the number of the book you would like to explore: "))
            if choice < 1 or choice > len(books):
                print("Invalid choice. Please enter a valid number.")
                continue
            
            selected_book = books[choice - 1]
            book_id = selected_book["_id"]
            book_title = selected_book["title"]
            
            # Ask user for chapter
            chapter = input(f"Which chapter of {book_title} are you interested in? ").strip()
            
            # Construct API URL
            api_url = f"{BASE_URL}{book_id}/{chapter}"
            
            # Make API request
            try:
                response = requests.get(api_url)
                response.raise_for_status()  # Raise an exception for bad status codes
            except requests.exceptions.RequestException as e:
                print(f"Error fetching data from the API: {str(e)}")
                continue
            
            # Process API response
            try:
                data = response.json()
                if "summary" in data:
                    summary = data["summary"]
                    # Print the formatted summary
                    print(f"\nSummary of {book_title} chapter {chapter}:")
                    print(f"--{summary}")
                else:
                    print(f"No summary found for {book_title} chapter {chapter}.")
            except ValueError:
                print(f"Invalid JSON response from the API for {book_title} chapter {chapter}.")
            
            # Ask if user wants to view another chapter
            choice = input("Would you like to view another (Y/N)? ").strip().lower()
            if choice != 'y':
                break
        
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            continue
    
    print("Thank you for using Book of Mormon Summary Tool!")

if __name__ == "__main__":
    main()
