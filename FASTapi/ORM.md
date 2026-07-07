## SQLAlchemy

- 安装sqlalchemy[async]
- 安装aiomysql异步数据库驱动

![image-20260318201721504](images/image-20260318201721504.png)

**SQLAlchemy 的优势**
SQLAlchemy 是 Python 社区中最成熟的 ORM 框架之一，它提供了两种主要的 API：

- Core API: 更接近底层 SQL，允许你构建复杂的查询和操作，灵活性极高。
- ORM API: 通过映射类和对象来操作数据库，更符合面向对象编程思想，易于理解和使用。

###  Engine (引擎)

`Engine` 是 SQLAlchemy 的核心组件，代表了数据库的连接。它是所有数据库交互的起点。它负责管理数据库连接池和执行 SQL 语句。

```python
onnect_URL = "mysql+pymysql://root:123456@localhost:3306/test?charset=utf8mb4"
#创建数据库引擎
engine = create_async_engine(connect_URL,
                            echo=True,  #可选输出sql日志
                            pool_size=10,  #连接池大小
                            max_overflow=10)  #最大溢出连接
                            
                            
```

### Session (会话)
Session 是应用程序与数据库交互的主要接口。它提供了持久化对象的管理、事务控制和查询功能。在 SQLAlchemy 中，通常使用 sessionmaker 来创建会话工厂。  
```python
from sqlalchemy.orm import sessionmaker

# 创建会话工厂
SessionLocal = sessionmaker(bind=engine)

# 创建会话实例
db_session = SessionLocal()

SessionLocal = sessionmaker(bind=engine,
                            class_=AsyncSession,#异步session
                            expire_on_commit=False)#永不释放
```

### Model (模型)

模型（Model）是 Python 类 ，它被映射到数据库中的表。通过 SQLAlchemy 的装饰器（如 `@declarative_base()` 和 `__tablename__`），你可以将类属性映射到表的列。

```python
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
#新写法  
class Book(Base):
    __tablename__ = 'books_std'
    id: Mapped[int] = mapped_column(primary_key=True)
    bookname: Mapped[str] = mapped_column(String(50), nullable=False)
    author : Mapped[str] = mapped_column(String(50), nullable=False)
    price : Mapped[float] = mapped_column(nullable=False)
    publisher : Mapped[str] = mapped_column(String(50), nullable=False)
```

### Relationship (关系)

`Relationship` 用于定义模型之间的关联关系，如一对多、多对一、多对多。这使得在 Python 对象中导航关联数据变得非常直观。

```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    user_id = Column(Integer, ForeignKey('users.id')) # 外键
    author = relationship("User") # 关系

```

#### Transaction (事务)

事务是一组数据库操作，要么全部成功，要么全部失败。SQLAlchemy 的 `Session` 默认自动管理事务，但在需要时也可以手动控制。

```python
try:
    # 执行一系列数据库操作
    db_session.add(new_user)
    db_session.commit() # 提交事务
except Exception as e:
    db_session.rollback() # 回滚事务
finally:
    db_session.close() # 关闭会话
```



### Query (查询) //不用这个

`Query` 对象用于从数据库中检索数据。它提供了丰富的方法来构建和执行查询。

```python
# 使用 session 查询所有用户
users = db_session.query(User).all()

# 查询特定用户
user = db_session.query(User).filter(User.email == 'john@example.com').first()

```

## 建表

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时执行的代码
    print("Starting up...")
    yield
    # 关闭时执行的代码
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)
```



这种方式在 FastAPI 0.93.0 之后是官方推荐的方式，而 `on_event` 虽然目前仍可用，但未来可能会被弃用。如果您使用的是较新版本的 FastAPI，建议切换到 `lifespan`。

```python
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database and tables initialized.")
## 在 SQLAlchemy 中，engine.begin() 返回的是一个异步连接上下文管理器（AsyncConnection 对象）。这个上下文管理器用于管理数据库连接，并确保连接在操作完成后正确关闭。
@app.on_envent("startup")
async def start_up():
    await init_db():
```

## 继承Base类

```python
#新定义方式
class Book(Base):
    __tablename__ = 'books_std'
    id: Mapped[int] = mapped_column(primary_key=True)
    bookname: Mapped[str] = mapped_column(String(50), nullable=False)
    author : Mapped[str] = mapped_column(String(50), nullable=False)
    price : Mapped[float] = mapped_column(nullable=False)
    publisher : Mapped[str] = mapped_column(String(50), nullable=False)
#老定义方式
class Post(Base):
    __tablename__ = 'posts_std'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, nullable=False) # 简化的外键
    created_at = Column(DateTime, default=datetime.utcnow)
```





## CRUD 操作详解

**Create**

```python
from sqlalchemy.orm import Session

def create_user(db: Session, name: str, email: str):
    """创建一个新用户"""
    db_user = User(name=name, email=email)
    db.add(db_user)
    db.commit() # 提交事务
    db.refresh(db_user) # 刷新对象，获取数据库中生成的 ID 等信息
    return db_user

# 使用示例
db_session = SessionLocal()
new_user = create_user(db_session, "Alice", "alice@example.com")
print(f"Created user: {new_user.name}, ID: {new_user.id}")
db_session.close()

```

### 新增

定义orm对象，添加对象到事务，然后commit到数据库。

```python
#将fastapi-Base对象转为dict然后解析给declarative_base

@app.post("/add_book")
async def add_book(book: Book, db: AsyncSession = Depends(get_database)):
    orm_book = my_orm.Book(**book.__dict__)
    db.add(orm_book)
    await db.commit()
    return book
```





### 查询

```python
#查询所有
@app.get("/book/{user_id}")
async def get_book(user_id: int, db: AsyncSession = Depends(get_database)):
    result = await db.execute(select(my_orm.Book))
    books = result.scalars().all()
    #找第一条
    books = result.scalars().first()
    return books
#查询单个user_id：主键值。如果是单列主键，直接传值（如 user_id）；如果是复合主键，传入一个元组，如 (id1, id2)。
@app.get("/book/{user_id}")
async def get_book(user_id: int, db: AsyncSession = Depends(get_database)):
    #result = await db.execute(select(my_orm.Book))
    #books = result.scalars().all()
    #books = result.scalars().first()
    books = await db.get(my_orm.Book, user_id)
    return books
```

![image-20260325151503571](images/image-20260325151503571.png)

```python
#比较判断
@app.get("/book/{user_id}")
async def get_book(user_id: int, db: AsyncSession = Depends(get_database)):
    result = await db.execute(select(my_orm.Book).where(my_orm.Book.id == user_id))
    books = result.scalar_one_or_none()
    return books
#模糊查询 % 是多个字符， - 是一个字符
#$需要加括号别忘了（）
@app.get("/book/{user_id}")
async def get_book(user_id: int, db: AsyncSession = Depends(get_database)):
    result = await db.execute(select(my_orm.Book).where((my_orm.Book.price >= int(10))&
                                                        (my_orm.Book.bookname.like("%月亮%"))))
    books = result.scalars().all()
    return books
#包含查询_in()
list = [1,2]
    result = await db.execute(select(my_orm.Book).where(my_orm.Book.id.in_(list)))  
```

### 聚合查询，一般用来做统计

聚合计算：func.方法（模型类.属性）

- count 统计行数量
- avg 求平均值
- max求最大值
- min求最小值
- sum求和

```python
@app.get("/book_price/{book_price}")
async def get_book_price(book_price: int, db: AsyncSession = Depends(get_database)):
    #result = await db.execute(select(func.count(my_orm.Book.id)))
    #result = await db.execute(select(func.sum(my_orm.Book.price)))
    result = await db.execute(select(func.avg(my_orm.Book.price)))
    count = result.scalar()
    return {"count": count}
```

### 分页查询

分页查询：select().offset().limit()

- offfset 跳过的记录数
- limit 返回的记录数

```python
@app.get("/book_name/{book_name}")
async def get_book_name(book_name: str, db: AsyncSession = Depends(get_database)):
    result = await db.execute(select(my_orm.Book).where(my_orm.Book.bookname.like(f"%%"))
                              .offset(0).limit(10))
    books = result.scalars().all()
    return books
```

![image-20260325171240863](images/image-20260325171240863.png)

### 更新数据

核心步骤，先查询，然后将属性重新赋值，commit到数据库。

```python
# 先查再改，后提交。
@app.post("/update_book")
async def update_book(book: Book, db: AsyncSession = Depends(get_database)):
    orm_book = await db.get(my_orm.Book, book.id)
    if not orm_book:
        raise HTTPException(status_code=404, detail="书籍不存在")
    db.execute(select(my_orm.Book).where(my_orm.Book.id == book.id))
    orm_book.bookname = book.bookname
    orm_book.author = book.author
    orm_book.price = book.price
    orm_book.publisher = book.publisher
    await db.commit()
    return book
```



### 删除操作

先查询，再删除，最后提交。

```python
#别忘记加await
@app.delete("/delete_book/{book_id}")
async def delete_book(book_id: int, db: AsyncSession = Depends(get_database)):
    book = await db.get(my_orm.Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="书籍不存在")
    await db.delete(book) 
    await db.commit()
    return {"message": "删除成功"}
```





## 路由中中如何使用ORM

创建依赖项，再dependence注入。

```python
#yilai
async def get_database():
    async with my_orm.SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
        finally:
            await session.close()
#luyou

```



