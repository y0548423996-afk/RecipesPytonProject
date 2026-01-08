USE master;
GO
CREATE DATABASE Recipes COLLATE hebrew_100_ci_as;
GO
USE Recipes ;
GO

CREATE TABLE categories (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100) NOT NULL UNIQUE
);
GO

CREATE TABLE recipes (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(200) NOT NULL,
    description NVARCHAR(MAX),
    ingredients NVARCHAR(MAX) NOT NULL,
    instructions NVARCHAR(MAX) NOT NULL,
    prep_time_minutes INT,
    servings INT,
    image_url NVARCHAR(500),
    category_id INT,
    created_at DATETIME DEFAULT GETDATE(),
    CONSTRAINT FK_Recipes_Categories
        FOREIGN KEY (category_id) REFERENCES categories(id)
);
GO





INSERT INTO categories (name)
VALUES (N'קינוחים'), (N'עוגות'), (N'ועוגיות'), (N'בריא')


INSERT INTO recipes
(name, description, ingredients, instructions, prep_time_minutes, servings, image_url, category_id)
VALUES
-- קינוחים
(N'מוס שוקולד קל',
 N'קינוח שוקולד רך ומהיר',
 N'שמנת מתוקה, שוקולד מריר',
 N'להמיס שוקולד, להקציף שמנת ולערבב',
 10,
 4,
 N'https://d3o5sihylz93ps.cloudfront.net/wp-content/uploads/sites/2/2019/08/04100526/shutterstock_225967111.jpg',
 1),

(N'כדורי תמרים ושוקולד',
 N'קינוח טבעי ללא אפייה',
 N'תמרים, קקאו, קוקוס',
 N'לטחון, ליצור כדורים ולקרר',
 10,
 6,
 N'https://www.10dakot.co.il/wp-content/uploads/2018/08/%E2%80%8F%E2%80%8FDSC_0111-%D7%A2%D7%95%D7%AA%D7%A7.jpg',
 1),

-- עוגות
(N'עוגת וניל אישית',
 N'עוגה אישית במיקרוגל',
 N'קמח, סוכר, ביצה, חלב, וניל',
 N'לערבב בספל ולחמם 2 דקות',
 5,
 1,
 N'https://www.10dakot.co.il/wp-content/uploads/2017/06/%E2%80%8F%E2%80%8FDSC_0054-%D7%A2%D7%95%D7%AA%D7%A7.jpg',
 2),

(N'עוגת שוקולד קלאסית',
 N'עוגת שוקולד פשוטה',
 N'קמח, סוכר, קקאו, ביצים',
 N'לערבב ולאפות 30 דקות',
 40,
 8,
 N'https://www.10dakot.co.il/wp-content/uploads/2013/07/%E2%80%8F%E2%80%8FDSC_0038-%D7%A2%D7%95%D7%AA%D7%A7.jpg',
 2),

-- ועוגיות
(N'עוגיות שיבולת שועל',
 N'עוגיות בריאות וקלות',
 N'שיבולת שועל, בננה, דבש',
 N'לערבב ולאפות 15 דקות',
 20,
 10,
 N'https://www.10dakot.co.il/wp-content/uploads/2013/09/20130927_114759.jpg',
 3),

(N'עוגיות חמאה',
 N'עוגיות פריכות וקלאסיות',
 N'קמח, חמאה, סוכר',
 N'ללוש, ליצור עוגיות ולאפות',
 30,
 15,
 N'https://www.10dakot.co.il/wp-content/uploads/2013/09/cookies-435296_1280.png',
 3),

(N'עוגיות שוקולד צ׳יפס',
 N'עוגיות רכות עם שוקולד',
 N'קמח, סוכר, שוקולד, ביצה',
 N'לערבב ולאפות 12 דקות',
 25,
 12,
 N'https://www.10dakot.co.il/wp-content/uploads/2019/07/%E2%80%8F%E2%80%8FDSC_0120-%D7%A2%D7%95%D7%AA%D7%A7.jpg',
 3),

-- בריא (ללא סלטים)
(N'שייק פירות טבעי',
 N'שייק מרענן ובריא',
 N'בננה, תות, חלב שקדים',
 N'לטחון הכול בבלנדר',
 5,
 2,
 N'https://www.10dakot.co.il/wp-content/uploads/2017/08/%E2%80%8F%E2%80%8F%D7%A9%D7%99%D7%99%D7%A7-%D7%A4%D7%99%D7%A8%D7%95%D7%AA-%D7%A2%D7%95%D7%AA%D7%A7.jpg',
 4),

(N'טורטיית חלבון',
 N'חטיף בריא מהיר',
 N'קמח שיבולת שועל, ביצה, חלבון אבקה',
 N'לערבב, לאפות 15 דקות',
 20,
 1,
 N'https://www.10dakot.co.il/wp-content/uploads/2016/03/DSC_0142-%D7%A2%D7%95%D7%AA%D7%A7.jpg',
 4),

(N'עוגת גזר קטנה',
 N'עוגה בריאה עם גזר',
 N'קמח מלא, גזר, ביצים, דבש',
 N'לערבב ולאפות 25 דקות',
 30,
 6,
 N'https://www.10dakot.co.il/wp-content/uploads/2013/10/%D7%A2%D7%95%D7%92%D7%AA-%D7%92%D7%96%D7%A8-%D7%9C%D7%9C%D7%90-%D7%92%D7%9C%D7%95%D7%98%D7%9F.jpg',
 4);



