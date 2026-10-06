## Задание 1

```bash
grep -o '^[^:]*' /etc/passwd | sort
```
o - слова целиком  
^[^:]* - от начала строки до двоеточия

## Задание 2

```bash
awk '!/^#/ && NF {print $2, $1}' /etc/protocols | sort -rn | head -n 5
```

!/^#/ - игнорирует коменатрии, NF - пустые строки  
rn - сортировка по числам и в обратном порядке

## Задание 3

```bash
#!/bin/bash
if [ "$#" -eq 0 ]; then
    echo "Использование: $0 <текст>" >&2
    exit 1
fi
text="$1"
length=${#text}
line="+"
for ((i = 0; i < length + 2; i++)); do
    line+="-"
done
line+="+"
printf '%s\n' "$line"
printf '| %s |\n' "$text"
printf '%s\n' "$line"
```

## Задание 4

```bash
#!/bin/bash
if [ "$#" -eq 0 ]; then
    echo "Использование: $0 <файл>" >&2
    exit 1
fi
grep -oE '[A-Za-z_][A-Za-z0-9_]*' "$1" | sort -u | paste -sd ' ' -
```

o - слова целиком  
E - расширенные регулярные выражения  
u - убирает дубликаты  
sd - вывод в строку через определенный символ (пробел)

## Задание 5

```bash
#!/bin/bash
if [ "$#" -ne 1 ]; then
        echo "Использование: $0 <файл>" >&2
        exit 1
fi
if [ ! -f "$1" ]; then
        echo "Ошибка: файл '$1' не найден" >&2
        exit 1
fi
chmod 755 "$1" || exit 1
cp "$1" /usr/local/bin/ || exit 1
echo "Команда '$(basename "$1")' установлена в /usr/local/bin"
```

f - существует и является файлом  
basename - отрезать путь, оставить только имя файла

## Задание 6

```bash
#!/bin/bash
if [ "$#" -ne 1 ]; then
        echo "Использование: $0 <файл>" >&2
        exit 1
fi
if [ ! -f "$1" ]; then
        echo "Ошибка: файл '$1' не найден" >&2
        exit 1
fi
first=$(head -n 1 "$1")
case "$1" in
        *.c|*.js)
                if [[ "$first" == //* || "$first" == /* ]]; then
                        echo "$1: комментарий"
                else
                        echo "$1: нет комментария"
                fi
                ;;
        *.py)
                if [[ "$first" == \#* ]]; then
                        echo "$1: комментарий"
                else
                        echo "$1: нет комментария:"
                fi
                ;;
        *)
                echo "$1: неизвестное расширение" >&2
                exit 2
                ;;
esac
```

f - существует и является файлом

## Задание 7

```bash
#!/bin/bash
find "$1" -type f -exec md5sum {} + 2>/dev/null | sort | uniq -d -w32
```

d w32 - только те строки которые дублируются и только первые 32 символа хэша

## Задание 8

```bash
#!/bin/bash
find . -type f -name "*.txt" > /tmp/filelist.txt
tar -f "txt.tar" -T /tmp/filelist.txt
COUNT=$(wc -l < /tmp/filelist.txt)
rm -f /tmp/filelist.txt
echo "Готово: txt.tar ($COUNT файлов)"
```

wc -l - считаь только количество строк  
f - принудительное удаление

## Задание 9

```bash
#!/bin/bash
sed 's/ \{4\}/t/g' "$1" > "$2"
```

t - табуляция
g - глобальная замена

## Задание 10

```bash
#!/bin/bash
find "$1" -type f -size 0
```
