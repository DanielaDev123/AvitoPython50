import random
from decimal import Decimal

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from avito_app.models import (
    UserProfile,
    Category,
    SubCategory,
    Product,
    ProductImage,
    Review,
)


def fake_file(name):
    return ContentFile(b"fake file content", name=name)


class Command(BaseCommand):
    help = "Заполняет базу тестовыми данными"

    def handle(self, *args, **options):
        self.stdout.write("Очистка старых данных...")
        Review.objects.all().delete()
        ProductImage.objects.all().delete()
        Product.objects.all().delete()
        SubCategory.objects.all().delete()
        Category.objects.all().delete()
        UserProfile.objects.filter(is_superuser=False).delete()

        self.stdout.write("Создание пользователей...")
        statuses = ['gold', 'silver', 'bronze', 'simple']
        first_names = ['Азамат', 'Бермет', 'Данияр', 'Гулмира', 'Эрлан',
                       'Айгерим', 'Максат', 'Нургуль', 'Тимур', 'Сайкал']
        last_names = ['Асанов', 'Токтогулова', 'Жумабеков', 'Абдырахманова',
                      'Мамбетов', 'Осмонова', 'Сыдыков', 'Кадырова',
                      'Бекболотов', 'Иманалиева']

        users = []
        for i in range(1, 11):
            user = UserProfile.objects.create_user(
                username=f'user{i}',
                password='password123',
                email=f'user{i}@example.com',
                first_name=first_names[i - 1],
                last_name=last_names[i - 1],
                age=random.randint(16, 60),
                phone_number=f'+99655500{i:04d}',
                status=random.choice(statuses),
            )
            user.avatar.save(f'avatar_{i}.jpg', fake_file(f'avatar_{i}.jpg'), save=True)
            users.append(user)

        self.stdout.write("Создание категорий...")
        category_names = [
            'Электроника', 'Одежда', 'Мебель', 'Транспорт', 'Недвижимость',
            'Хобби и отдых', 'Детские товары', 'Животные', 'Красота и здоровье',
            'Продукты питания',
        ]
        categories = []
        for name in category_names:
            cat = Category(category_name=name)
            cat.category_image.save(f'{name}.jpg', fake_file(f'{name}.jpg'), save=True)
            categories.append(cat)

        self.stdout.write("Создание подкатегорий...")
        subcategory_names = [
            'Смартфоны', 'Ноутбуки', 'Телевизоры', 'Куртки', 'Обувь',
            'Диваны', 'Столы', 'Автомобили', 'Квартиры', 'Велосипеды',
        ]
        subcategories = []
        for name in subcategory_names:
            sub = SubCategory(category=random.choice(categories), subcategory_name=name)
            sub.subcategory_image.save(f'{name}.jpg', fake_file(f'{name}.jpg'), save=True)
            subcategories.append(sub)

        self.stdout.write("Создание товаров...")
        product_names = [
            'iPhone 15', 'MacBook Air', 'Samsung TV 55"', 'Зимняя куртка',
            'Кроссовки Nike', 'Диван угловой', 'Обеденный стол', 'Toyota Camry',
            '2-комнатная квартира', 'Горный велосипед',
        ]
        products = []
        for i, name in enumerate(product_names, start=1):
            product = Product(
                sub_category=random.choice(subcategories),
                product_name=name,
                price=Decimal(random.randrange(500, 500000)) / 100,
                description=f'Описание товара: {name}. Отличное состояние, торг уместен.',
                article_number=100000 + i,
                product_type=random.choice([True, False]),
            )
            product.video.save(f'{name}_video.mp4', fake_file(f'{name}_video.mp4'), save=True)
            products.append(product)

        self.stdout.write("Создание изображений товаров...")
        for i in range(1, 11):
            product = random.choice(products)
            pi = ProductImage(product=product)
            pi.product_image.save(f'product_{i}.jpg', fake_file(f'product_{i}.jpg'), save=True)

        self.stdout.write("Создание отзывов...")
        comments = [
            'Отличный товар, рекомендую!', 'Качество на высоте.',
            'Немного дороговато, но того стоит.', 'Быстрая доставка, всё понравилось.',
            'Есть небольшие недостатки, но в целом хорошо.', 'Буду заказывать ещё.',
            'Не совсем то, что ожидал.', 'Соответствует описанию.',
            'Продавец очень отзывчивый.', 'Топовый товар!',
        ]
        for i in range(10):
            Review.objects.create(
                user=random.choice(users),
                product=random.choice(products),
                comment=comments[i],
                stars=random.randint(1, 5),
            )

        self.stdout.write(self.style.SUCCESS("Готово! База данных успешно заполнена."))