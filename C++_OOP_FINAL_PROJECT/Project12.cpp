#include <iostream>
#include <fstream>
#include <cstring>

using namespace std;

struct FileMeta {
    char fileName[50];
    int sizeKB;
};

// Abstract base class
class IndexEntry {
public:
    FileMeta meta;

    IndexEntry(const char* name, int size) {
        strncpy(meta.fileName, name, 49);
        meta.fileName[49] = '\0';
        meta.sizeKB = size;
    }

    virtual void printEntry() = 0;
    virtual const char* getName() = 0;
    virtual const char* getType() = 0;
    virtual void saveToFile(ofstream& out) = 0;
    virtual ~IndexEntry() {}
};

// TextFile class
class TextFile : public IndexEntry {
    int* wordCount;
public:
    TextFile(const char* name, int size, int words)
        : IndexEntry(name, size) {
        wordCount = new int(words);
    }

    void printEntry() override {
        cout << "Text File: " << meta.fileName
             << ", Size: " << meta.sizeKB
             << "KB, Word Count: " << *wordCount << endl;
    }

    const char* getName() override {
        return meta.fileName;
    }

    const char* getType() override {
        return "TextFile";
    }

    void saveToFile(ofstream& out) override {
        out << "TextFile|" << meta.fileName << "|" << meta.sizeKB << "|" << *wordCount << endl;
    }

    ~TextFile() {
        delete wordCount;
    }
};

// ImageFile class
class ImageFile : public IndexEntry {
    int* width;
    int* height;
public:
    ImageFile(const char* name, int size, int w, int h)
        : IndexEntry(name, size) {
        width = new int(w);
        height = new int(h);
    }

    void printEntry() override {
        cout << "Image File: " << meta.fileName
             << ", Size: " << meta.sizeKB
             << "KB, Width: " << *width
             << ", Height: " << *height << endl;
    }

    const char* getName() override {
        return meta.fileName;
    }

    const char* getType() override {
        return "ImageFile";
    }

    void saveToFile(ofstream& out) override {
        out << "ImageFile|" << meta.fileName << "|" << meta.sizeKB << "|" << *width << "|" << *height << endl;
    }

    ~ImageFile() {
        delete width;
        delete height;
    }
};

// File Indexer with dynamic array
class FileIndexer {
    IndexEntry** entries;
    int count;

public:
    FileIndexer() : entries(nullptr), count(0) {}

    void addEntry(IndexEntry* entry) {
        IndexEntry** newEntries = new IndexEntry*[count + 1];
        for (int i = 0; i < count; ++i)
            newEntries[i] = entries[i];
        newEntries[count] = entry;
        delete[] entries;
        entries = newEntries;
        count++;
    }

    void removeEntry(const char* name) {
        int index = -1;
        for (int i = 0; i < count; ++i) {
            if (strcmp(entries[i]->getName(), name) == 0) {
                index = i;
                break;
            }
        }
        if (index == -1) {
            cout << "File not found.\n";
            return;
        }

        delete entries[index];

        IndexEntry** newEntries = new IndexEntry*[count - 1];
        for (int i = 0, j = 0; i < count; ++i) {
            if (i != index)
                newEntries[j++] = entries[i];
        }

        delete[] entries;
        entries = newEntries;
        count--;

        cout << "File removed successfully.\n";
    }

    void printAll() {
        if (count == 0) {
            cout << "No entries to display.\n";
            return;
        }
        for (int i = 0; i < count; ++i)
            entries[i]->printEntry();
    }

    void saveToFile(const char* filename) {
        ofstream out(filename);
        if (!out) {
            cout << "Error opening file for writing.\n";
            return;
        }
        for (int i = 0; i < count; ++i)
            entries[i]->saveToFile(out);
        out.close();
        cout << "Entries saved to file.\n";
    }

    void loadFromFile(const char* filename) {
        ifstream in(filename);
        if (!in) {
            cout << "No existing file found, starting fresh.\n";
            return;
        }

        char line[256];
        while (in.getline(line, 256)) {
            char* type = strtok(line, "|");
            char* name = strtok(nullptr, "|");
            char* sizeStr = strtok(nullptr, "|");

            if (strcmp(type, "TextFile") == 0) {
                char* wordCountStr = strtok(nullptr, "|");
                addEntry(new TextFile(name, atoi(sizeStr), atoi(wordCountStr)));
            }
            else if (strcmp(type, "ImageFile") == 0) {
                char* widthStr = strtok(nullptr, "|");
                char* heightStr = strtok(nullptr, "|");
                addEntry(new ImageFile(name, atoi(sizeStr), atoi(widthStr), atoi(heightStr)));
            }
        }
        in.close();
        cout << "Entries loaded from file.\n";
    }

    ~FileIndexer() {
        for (int i = 0; i < count; ++i)
            delete entries[i];
        delete[] entries;
    }
};

// User-driven menu
void menu(FileIndexer& indexer) {
    int choice;
    do {
        cout << "\n---- File Indexing System ----\n";
        cout << "1. Add Text File\n";
        cout << "2. Add Image File\n";
        cout << "3. Remove File\n";
        cout << "4. Show All Entries\n";
        cout << "5. Save to File\n";
        cout << "6. Exit\n";
        cout << "Enter your choice: ";
        cin >> choice;

        char name[50];
        int size, words, width, height;

        switch (choice) {
            case 1:
                cout << "Enter file name: ";
                cin >> name;
                cout << "Enter size in KB: ";
                cin >> size;
                cout << "Enter word count: ";
                cin >> words;
                indexer.addEntry(new TextFile(name, size, words));
                break;

            case 2:
                cout << "Enter file name: ";
                cin >> name;
                cout << "Enter size in KB: ";
                cin >> size;
                cout << "Enter width: ";
                cin >> width;
                cout << "Enter height: ";
                cin >> height;
                indexer.addEntry(new ImageFile(name, size, width, height));
                break;

            case 3:
                cout << "Enter file name to remove: ";
                cin >> name;
                indexer.removeEntry(name);
                break;

            case 4:
                indexer.printAll();
                break;

            case 5:
                indexer.saveToFile("files.txt");
                break;

            case 6:
                cout << "Exiting program...\n";
                break;

            default:
                cout << "Invalid choice. Try again.\n";
        }

    } while (choice != 6);
}

// MAIN
int main() {
    FileIndexer indexer;
    indexer.loadFromFile("files.txt"); // load existing entries
    menu(indexer); // launch user interface
    indexer.saveToFile("files.txt"); // save before exit
    return 0;
}


