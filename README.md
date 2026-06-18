# 💅 Salon Smart – AWS Edition

מערכת לניהול תורים לסטודיו ציפורניים, מבוססת על ארכיטקטורה Serverless מלאה ב-AWS.

## 🎯 תיאור הפרויקט

Salon Smart היא מערכת אוטומטית המאפשרת ללקוחות לקבוע, לבטל ולנהל תורים באופן עצמאי 24/7, תוך שחרור בעלת העסק מניהול שוטף.

## 🏗️ ארכיטקטורת AWS

לקוחה → S3 (UI) → API Gateway → Lambda → DynamoDB → SES / SNS / CloudWatch

## ☁️ שירותי AWS בשימוש

| שירות | תפקיד | סוג |
|-------|--------|-----|
| Amazon S3 | אחסון ממשק המשתמש הסטטי | חובה |
| API Gateway | חשיפת REST API | חובה |
| AWS Lambda | לוגיקה עסקית (Python 3.12) | חובה |
| Amazon DynamoDB | בסיס נתונים (תורים, לקוחות, שירותים) | חובה |
| AWS IAM | ניהול הרשאות | חובה |
| Amazon SES | שליחת מיילי אישור | בחירה |
| Amazon SNS | התראות למנהלת | בחירה |
| Amazon CloudWatch | ניטור ולוגים | בחירה |

## 📁 מבנה הקבצים

index.html - ממשק המשתמש
lambda_function.py - קוד ה-Lambda
lambda.zip - קובץ הפריסה

## 🚀 הוראות התקנה

### דרישות מקדימות
- חשבון AWS
- AWS CLI מותקן ומוגדר
- Git מותקן

### שלבי התקנה

1. יצירת טבלאות DynamoDB:
aws dynamodb create-table --table-name Appointments --attribute-definitions AttributeName=appointment_id,AttributeType=S --key-schema AttributeName=appointment_id,KeyType=HASH --billing-mode PAY_PER_REQUEST --region us-east-1
aws dynamodb create-table --table-name Services --attribute-definitions AttributeName=service_id,AttributeType=S --key-schema AttributeName=service_id,KeyType=HASH --billing-mode PAY_PER_REQUEST --region us-east-1
aws dynamodb create-table --table-name Clients --attribute-definitions AttributeName=client_phone,AttributeType=S --key-schema AttributeName=client_phone,KeyType=HASH --billing-mode PAY_PER_REQUEST --region us-east-1

2. יצירת Lambda Role:
aws iam create-role --role-name salon-smart-lambda-role --assume-role-policy-document ...

3. יצירת פונקציית Lambda:
aws lambda create-function --function-name salon-smart-api --runtime python3.12 --role arn:aws:iam::417441750937:role/salon-smart-lambda-role --handler lambda_function.lambda_handler --zip-file fileb://lambda.zip --region us-east-1

4. יצירת API Gateway:
aws apigatewayv2 create-api --name salon-smart-api --protocol-type HTTP --region us-east-1

5. העלאת האתר ל-S3:
aws s3 cp index.html s3://salon-smart-website-417441750937/ --region us-east-1

## 🌐 כתובת האתר החי

http://salon-smart-website-417441750937.s3-website-us-east-1.amazonaws.com

## 📊 Use Cases

1. לקוחה קובעת תור – בוחרת שירות, תאריך ושעה ומקבלת אישור
2. לקוחה מבטלת תור – ביטול עצמאי עם אישור במייל
3. לקוחה מקבלת מידע על שירותים – מחירים ומשך טיפולים
4. מנהלת צופה בלוח תורים – דרך פאנל הניהול
5. מנהלת מאשרת בקשה דחופה – התראת SNS על תורים קרובים
6. שליחת אישור אוטומטי – מייל ללקוחה דרך SES
7. ניטור המערכת – CloudWatch מתעד לוגים והתראות

## 👩‍💻 פרטי הפרויקט

- **שם:** Salon Smart – AWS Edition
- **קורס:** ניהול מערכות ענן (AWS)
- **מרצה:** אורי ברמן
- **מוסד:** מכללת עזריאלי ירושלים
- **שנה:** תשפ"ו
- **פותח על ידי:** תמר
