from rest_framework import serializers
from .models import Book, Category, Order

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'books', 'total_price', 'ordered_at']

    def create(self, validated_data):
        books = validated_data.pop('books')
        order = Order.objects.create(**validated_data)
        
        total_price = 0
        for book in books:
            quantity = 1  # Assuming 1 item per book
            # Check if stock is available
            if book.stock < quantity:
                raise serializers.ValidationError(f"Not enough stock for {book.title}. Available: {book.stock}")
            
            # Reduce stock
            book.stock -= quantity
            book.save()

            total_price += book.price * quantity

        order.total_price = total_price
        order.save()

        return order
