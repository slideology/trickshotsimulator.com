import os
from app import app, db
from models import User, PricingPlan

def init_db():
    # 删除现有的数据库文件
    db_path = os.path.join(app.instance_path, 'windsurf.db')
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Removed existing database at {db_path}")

    # 确保instance目录存在
    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)
        print(f"Created instance directory at {app.instance_path}")

    with app.app_context():
        # 删除所有表并重新创建
        db.drop_all()
        db.create_all()
        print("Created all database tables")

        # 创建测试用户
        test_user = User(username='test', email='test@example.com')
        test_user.set_password('password')
        db.session.add(test_user)
        print("Created test user")

        # 创建定价计划
        plans = [
            PricingPlan(
                name='Basic Package',
                description='Perfect for getting started',
                price=9.99,
                credits=100,
                is_subscription=False
            ),
            PricingPlan(
                name='Pro Package',
                description='Most popular choice for regular users',
                price=24.99,
                credits=300,
                is_subscription=False
            ),
            PricingPlan(
                name='Premium Subscription',
                description='Best value for power users',
                price=49.99,
                credits=1000,
                is_subscription=True
            )
        ]
        
        for plan in plans:
            db.session.add(plan)
        print("Created pricing plans")

        # 提交所有更改
        try:
            db.session.commit()
            print("Successfully initialized the database!")
        except Exception as e:
            print(f"Error initializing database: {e}")
            db.session.rollback()

if __name__ == '__main__':
    init_db()
