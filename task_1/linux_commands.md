# Linux Commands Documentation

## 1. pwd

Command:

```bash
pwd
```

Purpose:
Displays the current working directory.

Observed Output:

```text
/home/user/Synergy_TP
```

---

## 2. ls

Command:

```bash
ls
```

Purpose:
Lists files and folders in the current directory.

Observed Output:

```text
task_1  task_2
```

---

## 3. ls -la

Command:

```bash
ls -la
```

Purpose:
Lists all files including hidden files.

Observed Output:

```text
drwxr-xr-x task_1
drwxr-xr-x task_2
-rw-r--r-- .gitignore
```

---

## 4. cd

Command:

```bash
cd task_1
```

Purpose:
Changes the current directory.

Observed Output:

```text
Current directory changed to task_1
```

---

## 5. mkdir

Command:

```bash
mkdir demo
```

Purpose:
Creates a new directory.

Observed Output:

```text
Directory 'demo' created
```

---

## 6. touch

Command:

```bash
touch file.txt
```

Purpose:
Creates an empty file.

Observed Output:

```text
file.txt created
```

---

## 7. cat

Command:

```bash
cat sample.txt
```

Purpose:
Displays contents of a file.

Observed Output:

```text
This is a sample file for Task 1.
```

---

## 8. echo

Command:

```bash
echo Hello
```

Purpose:
Prints text to terminal.

Observed Output:

```text
Hello
```

---

## 9. cp

Command:

```bash
cp file.txt copy.txt
```

Purpose:
Copies a file.

Observed Output:

```text
copy.txt created
```

---

## 10. mv

Command:

```bash
mv copy.txt renamed.txt
```

Purpose:
Moves or renames files.

Observed Output:

```text
copy.txt renamed to renamed.txt
```

---

## 11. rm

Command:

```bash
rm renamed.txt
```

Purpose:
Deletes a file.

Observed Output:

```text
renamed.txt removed
```

---

## 12. grep

Command:

```bash
grep Hello sample.txt
```

Purpose:
Searches for matching text.

Observed Output:

```text
Hello
```

---

## 13. find

Command:

```bash
find . -name "*.py"
```

Purpose:
Finds files matching a pattern.

Observed Output:

```text
./src/hello.py
```

---

## 14. head

Command:

```bash
head sample.txt
```

Purpose:
Displays first lines of a file.

Observed Output:

```text
This is a sample file for Task 1.
```

---

## 15. tail

Command:

```bash
tail sample.txt
```

Purpose:
Displays last lines of a file.

Observed Output:

```text
This is a sample file for Task 1.
```

---

## 16. wc

Command:

```bash
wc sample.txt
```

Purpose:
Counts lines, words, and characters.

Observed Output:

```text
1 7 33 sample.txt
```

---

## 17. chmod

Command:

```bash
chmod +x script.sh
```

Purpose:
Changes file permissions.

Observed Output:

```text
Permissions updated successfully
```