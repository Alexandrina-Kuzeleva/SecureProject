# Report Task1

## 1. Скриншот структуры проекта

### Создание структуры и файлов, проверка secret_plan.txt и копирование, grep и evidence.log
![Скриншот 1](screenshots/Снимок%20экрана%202026-02-12%20170337.png)
![Скриншот 2](screenshots/Снимок%20экрана%202026-02-12%20170811.png)

### sudo apt update и установка tree
![Скриншот 3](screenshots/Снимок%20экрана%202026-02-12%20171111.png)
![Скриншот 4](screenshots/Снимок%20экрана%202026-02-12%20171146.png)

### tree
![Скриншот 5](screenshots/Снимок%20экрана%202026-02-12%20171222.png)

### history
![Скриншот 6](screenshots/Снимок%20экрана%202026-02-12%20171254.png)

## 2. Содержимое evidence.log
```/home/alexandrina/secure_project/backup/secret_plan_v1.txt: The password is 12345```


## 3. История выполненных команд

1. cd ~
2. mkdir -p ~/secure_project/docs ~/secure_project/src ~/secure_project/backup
3. ls
4. cd secure_project
5. ls
6. cd ..
7. echo "The password is 12345" > ~/secure_project/docs/secret_plan.txt
8. cd secure_project/docs
9. ls
10. cat secret_plan.txt
11. cp ~/secure_project/docs/secret_plan.txt ~/secure_project/backup/secret_plan_v1.txt
12. cd ..
13. cd backup
14. ls
15. cat secret_lan_v1.txt
16. cat secret_plan_v1.txt
17. grep -r "password" ~/secure_project/backup >~/secure_project/evidence. log
18. cd
19. ls
20. cat evidence. log
21. sudo apt update
22. sudo apt install tree -y
23. tree ~/secure_project > ~/secure_project/report.txt
24. cat ~/secure_project/report.txt
25. history
