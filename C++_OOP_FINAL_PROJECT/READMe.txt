 File Indexing System - C++ Exam Project

 Project12 Title: File Indexing System

 Description of the Assigned Task

A student(I) have to create a file indexing system where:

* Text and image files hold different metadata.
* These are stored in a dynamic array for polymorphic behavior.
 I must:

  * Define a struct `FileMeta { char fileName[50]; int sizeKB; };`
  * Create an abstract class `IndexEntry` with a pure virtual function `printEntry()`.
  * Derive two classes:

    * `TextFile` which adds `int* wordCount`
    * `ImageFile` which adds `int* width`, `*height`
  * Store entries in a dynamic array of `IndexEntry**`
  * Implement functions to add and remove entries using pointer arithmetic and dynamic memory
  * Ensure user input/output and file saving/loading are implemented

---

##  How the Project Was Completed

 Step 1: Defining Common File Metadata


// Struct to store the basic metadata for all file types
struct FileMeta {
    char fileName[50]; // C-style string for filename (max 49 characters + null terminator)
    int sizeKB;        // File size in kilobytes
};


 Step 2: Abstract Class with Virtual Function


// Abstract base class for polymorphic behavior
class IndexEntry {
public:
    FileMeta meta; // Common metadata for both text and image files
public:
    virtual void printEntry() = 0;       // Must be implemented by derived classes
    virtual const char* getName() = 0;   // For comparing file names
    virtual void saveToFile(ofstream& out) = 0; // File persistence
    virtual ~IndexEntry() {}             // Virtual destructor for safe deletion
};
```

 Step 3: Inheritance - TextFile and ImageFile


// Derived class for text file entries
class TextFile : public IndexEntry {
    int* wordCount; // Pointer to word count
public:
    // Constructor initializes metadata and allocates memory for wordCount
    TextFile(const char* name, int size, int words) {
        strncpy(meta.fileName, name, 49); // Copy name safely
        meta.sizeKB = size;               // Assign size
        wordCount = new int(words);       // Dynamically allocate word count
    }

    // Prints the details of the text file
    void printEntry() override {
        cout << "TextFile: " << meta.fileName << ", " << meta.sizeKB << "KB, Words: " << *wordCount << endl;
    }

    // Returns the file name for comparison
    const char* getName() override {
        return meta.fileName;
    }

    // Saves the entry to file in a specific format
    void saveToFile(ofstream& out) override {
        out << "TextFile|" << meta.fileName << "|" << meta.sizeKB << "|" << *wordCount << endl;
    }

    // Destructor to free allocated memory
    ~TextFile() {
        delete wordCount;
    }
};



// Derived class for image file entries
class ImageFile : public IndexEntry {
    int* width;  // Pointer to width
    int* height; // Pointer to height
public:
    // Constructor initializes metadata and dimensions
    ImageFile(const char* name, int size, int w, int h) {
        strncpy(meta.fileName, name, 49); // Copy file name
        meta.sizeKB = size;
        width = new int(w);
        height = new int(h);
    }

    // Print image file details
    void printEntry() override {
        cout << "ImageFile: " << meta.fileName << ", " << meta.sizeKB << "KB, " << *width << "x" << *height << endl;
    }

    // Return name for removal comparison
    const char* getName() override {
        return meta.fileName;
    }

    // Save metadata to file
    void saveToFile(ofstream& out) override {
        out << "ImageFile|" << meta.fileName << "|" << meta.sizeKB << "|" << *width << "|" << *height << endl;
    }

    // Destructor to deallocate width and height
    ~ImageFile() {
        delete width;
        delete height;
    }
};


 Step 4: Dynamic Entry Storage and Resizing


// Class to manage the collection of IndexEntry objects
class FileIndexer {
    IndexEntry** entries; // Dynamic array of pointers to entries
    int count;            // Total number of entries
public:
    FileIndexer() : entries(nullptr), count(0) {}

    // Adds a new entry, resizing the array
    void addEntry(IndexEntry* entry) {
        IndexEntry** newArray = new IndexEntry*[count + 1]; // New array with extra space
        for (int i = 0; i < count; i++) newArray[i] = entries[i]; // Copy old entries
        newArray[count++] = entry;  // Add new entry and update count
        delete[] entries;           // Delete old array
        entries = newArray;         // Point to new array
    }

    // Removes entry by name
    void removeEntry(const char* name) {
        int index = -1;
        for (int i = 0; i < count; i++) {
            if (strcmp(entries[i]->getName(), name) == 0) {
                index = i; // Found index to remove
                break;
            }
        }
        if (index == -1) return; // Entry not found

        delete entries[index]; // Free memory of entry
        IndexEntry** newArray = new IndexEntry*[count - 1]; // New array without the entry
        for (int i = 0, j = 0; i < count; i++) {
            if (i != index) newArray[j++] = entries[i]; // Skip the deleted entry
        }
        delete[] entries;
        entries = newArray;
        count--;
    }

    // Display all entries
    void showAll() {
        for (int i = 0; i < count; i++) entries[i]->printEntry();
    }

    // Save all entries to a file
    void saveToFile(const char* filename) {
        ofstream out(filename);
        for (int i = 0; i < count; i++) entries[i]->saveToFile(out);
        out.close();
    }

    // Load entries from a file
    void loadFromFile(const char* filename) {
        ifstream in(filename);
        if (!in) return;
        string line;
        while (getline(in, line)) {
            stringstream ss(line);
            string type;
            getline(ss, type, '|');
            if (type == "TextFile") {
                string name; int size, words;
                getline(ss, name, '|'); ss >> size; ss.ignore(); ss >> words;
                addEntry(new TextFile(name.c_str(), size, words));
            } else if (type == "ImageFile") {
                string name; int size, w, h;
                getline(ss, name, '|'); ss >> size; ss.ignore(); ss >> w; ss.ignore(); ss >> h;
                addEntry(new ImageFile(name.c_str(), size, w, h));
            }
        }
        in.close();
    }

    // Destructor to free all entries
    ~FileIndexer() {
        for (int i = 0; i < count; i++) delete entries[i];
        delete[] entries;
    }
};


  Step 5: User Interface Menu


// Interactive menu function for user input/output
void menu(FileIndexer& indexer) {
    int choice;
    do {
        cout << "\n1. Add TextFile\n2. Add ImageFile\n3. Remove Entry\n4. Show All\n5. Save\n6. Exit\nChoice: ";
        cin >> choice;

        if (choice == 1) {
            // Collect details for text file
            char name[50]; int size, words;
            cout << "Enter name, size, word count: ";
            cin >> name >> size >> words;
            indexer.addEntry(new TextFile(name, size, words));

        } else if (choice == 2) {
            // Collect details for image file
            char name[50]; int size, w, h;
            cout << "Enter name, size, width, height: ";
            cin >> name >> size >> w >> h;
            indexer.addEntry(new ImageFile(name, size, w, h));

        } else if (choice == 3) {
            // Remove an entry by name
            char name[50];
            cout << "Enter name to remove: ";
            cin >> name;
            indexer.removeEntry(name);

        } else if (choice == 4) {
            // Show all entries
            indexer.showAll();

        } else if (choice == 5) {
            // Save all entries to file
            indexer.saveToFile("files.txt");
        }
    } while (choice != 6); // Exit when user chooses 6
}


 Step 6: `main()` Entry


// Main function to run the indexing system
int main() {
    FileIndexer indexer;
    indexer.loadFromFile("files.txt"); // Load previously saved entries
    menu(indexer);                      // Show menu to user
    indexer.saveToFile("files.txt");   // Save current session
    return 0;
}



 Output Screenshots


1. Program Startup

    Loads previous data from `files.txt`

2. Add TextFile and ImageFile

    Shows success prompts and confirms entries added

3. View All Entries

    Uses `printEntry()` polymorphically

4. Remove Entry by Name

    Deletes a specific file from index

5. Save to File

    Stores all entries in `files.txt`

6. Exit

    Saves automatically before exiting



** Summary

This system demonstrates real-world use of object-oriented programming with C++ using polymorphism, file I/O, dynamic arrays, and pointer management. It’s interactive, extensible, and demonstrates clean C++ practices at a beginner-friendly level.

