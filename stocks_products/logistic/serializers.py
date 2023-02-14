from rest_framework import serializers

from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    # настройте сериализатор для продукта
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']
        #extra_kwargs = {'title': {'write_only': True}}

    def create(self, validated_data):
        id = Product.objects.update_or_create(**validated_data)
        return id[0].id

    def update(self, instance, validated_data):
        Product.objects.update_or_create(id=instance.id, defaults=validated_data)
        return validated_data


class ProductPositionSerializer(serializers.ModelSerializer):
    # настройте сериализатор для позиции продукта на складе
    class Meta:
        model = StockProduct
        exclude = ("id","stock",)


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    # настройте сериализатор для склада
    class Meta:
        model = Stock
        fields = '__all__'

    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')
        # создаем склад по его параметрам
        stock = super().create(validated_data)
        # здесь вам надо заполнить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions
        for position in positions:
            StockProduct.objects.create(stock_id=stock.id, product_id=position['product'].id, quantity=position['quantity'], price=position['price'])
        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')
        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)
        # здесь вам надо обновить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions
        for position in positions:
            StockProduct.objects.update_or_create(stock_id=stock.id, product_id=position['product'].id, defaults={'quantity':position['quantity'], 'price':position['price']})
        # Старый код до правки
        # for position in positions:
        #     StockProduct.objects.filter(stock_id=stock.id, product_id=position['product'].id).update(quantity=position['quantity'], price=position['price'])
        return stock
