# coding=utf-8

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, Category, Book

engine = create_engine('sqlite:///books.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create Dummy User
User1 = User(
    name="Benjamin Franklin",
    email="ben@franklin.com",
    picture="https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/BenFranklinDuplessis.jpg/1024px-BenFranklinDuplessis.jpg")
session.add(User1)
session.commit()

# Add all categories

# Books for Literary & Fiction

category1 = Category(name="Literary and Fiction")
session.add(category1)
session.commit()

book1 = Book(
    user_id=1,
    title="The Sympathizer: A Novel",
    author="Viet Thanh Nguyen",
    img="https://images-na.ssl-images-amazon.com/images/I/518LdNuHDJL._SX331_BO1,204,203,200_.jpg",
    category=category1)
session.add(book1)
session.commit()

book2 = Book(
    user_id=1,
    title="Hamilton: The Revolution",
    author="Lin-Manuel Miranda",
    img="https://images-na.ssl-images-amazon.com/images/I/51PK6V0aiOL._SX396_BO1,204,203,200_.jpg",
    category=category1)
session.add(book2)
session.commit()

book3 = Book(
    user_id=1,
    title="The Sellout: A Novel",
    author="Paul Beatty",
    img="https://images-na.ssl-images-amazon.com/images/I/51hEHDap2CL._SX324_BO1,204,203,200_.jpg",
    category=category1)
session.add(book3)
session.commit()

book4 = Book(
    user_id=1,
    title="Hot Milk",
    author="Deborah Levy",
    img="https://images-na.ssl-images-amazon.com/images/I/51FJvTjak1L._SX329_BO1,204,203,200_.jpg",
    category=category1)
session.add(book4)
session.commit()

# Books for Self Help

category2 = Category(name="Self Help")
session.add(category2)
session.commit()

book1 = Book(
    user_id=1,
    title="Rising Strong: The Reckoning. The Rumble. The Revolution.",
    author="Brené Brown",
    img="https://images-na.ssl-images-amazon.com/images/I/51K5xunS2RL._SX332_BO1,204,203,200_.jpg",
    category=category2)
session.add(book1)
session.commit()

book2 = Book(
    user_id=1,
    title="Trauma Stewardship: An Everyday Guide to Caring for Self While Caring for Others",
    author="Laura Van Dernoot Lipsky, Connie Burk",
    img="https://images-na.ssl-images-amazon.com/images/I/51hy9DeJdZL._SX332_BO1,204,203,200_.jpg",
    category=category2)
session.add(book2)
session.commit()

book3 = Book(
    user_id=1,
    title="Drive: The Surprising Truth About What Motivates Us",
    author="Daniel H. Pink",
    img="https://images-na.ssl-images-amazon.com/images/I/51sYIj%2Bc85L._SX332_BO1,204,203,200_.jpg",
    category=category2)
session.add(book3)
session.commit()

book4 = Book(
    user_id=1,
    title="The Power of Habit: Why We Do What We Do in Life and Business",
    author="Charles Duhigg",
    img="https://images-na.ssl-images-amazon.com/images/I/51NzjhIhK0L._SX322_BO1,204,203,200_.jpg",
    category=category2)
session.add(book4)
session.commit()

# Books for Childrens
category3 = Category(name="Childrens")
session.add(category3)
session.commit()

book1 = Book(
    user_id=1,
    title="The Very Hungry Caterpillar",
    author="Eric Carle",
    img="https://images-na.ssl-images-amazon.com/images/I/41zqrOnjpTL._SY343_BO1,204,203,200_.jpg",
    category=category3)
session.add(book1)
session.commit()

book2 = Book(
    user_id=1,
    title="Goodnight Moon",
    author="Margaret Wise Brown, Clement Hurd",
    img="https://images-na.ssl-images-amazon.com/images/I/51%2BmV1XUUQL._SY432_BO1,204,203,200_.jpg",
    category=category3)
session.add(book2)
session.commit()

book3 = Book(
    user_id=1,
    title="Brown Bear, Brown Bear, What Do You See?",
    author="Bill Martin Jr., Eric Carle",
    img="https://images-na.ssl-images-amazon.com/images/I/51430n%2B9jlL._SX355_BO1,204,203,200_.jpg",
    category=category3)
session.add(book3)
session.commit()

book4 = Book(
    user_id=1,
    title="The Giving Tree",
    author="Shel Silverstein",
    img="https://images-na.ssl-images-amazon.com/images/I/516dsrPeFDL._SX375_BO1,204,203,200_.jpg",
    category=category3)
session.add(book4)
session.commit()

# Books for Business
category4 = Category(name="Business")
session.add(category4)
session.commit()

book1 = Book(
    user_id=1,
    title="The ONE Thing: The Surprisingly Simple Truth Behind Extraordinary Results",
    author="Gary Keller, Jay Papasan",
    img="https://images-na.ssl-images-amazon.com/images/I/31NOChpx3CL.jpg",
    category=category4)
session.add(book1)
session.commit()

book2 = Book(
    user_id=1,
    title="Manage Your Day-to-Day: Build Your Routine, Find Your Focus, and Sharpen Your Creative Mind (The 99U Book Series)",
    author="Jocelyn K. Glei",
    img="https://images-na.ssl-images-amazon.com/images/I/51gpnuHI4-L.jpg",
    category=category4)
session.add(book2)
session.commit()

book3 = Book(
    user_id=1,
    title="Tools of Titans: The Tactics, Routines, and Habits of Billionaires, Icons, and World-Class Performers",
    author="Timothy Ferriss",
    img="https://images-na.ssl-images-amazon.com/images/I/51M-tW14QgL._SX387_BO1,204,203,200_.jpg",
    category=category4)
session.add(book3)
session.commit()

book4 = Book(
    user_id=1,
    title="StrengthsFinder 2.0",
    author="Tom Rath",
    img="https://images-na.ssl-images-amazon.com/images/I/41EII0L2ciL._SX360_BO1,204,203,200_.jpg",
    category=category4)
session.add(book4)
session.commit()

# Books for History
category5 = Category(name="History")
session.add(category5)
session.commit()

book1 = Book(
    user_id=1,
    title="The Professor and the Madman",
    author="Simon Winchester",
    img="https://images-na.ssl-images-amazon.com/images/I/51dWj7sjO4L._SX325_BO1,204,203,200_.jpg",
    category=category5)
session.add(book1)
session.commit()

book2 = Book(
    user_id=1,
    title="Three Days in January: Dwight Eisenhower's Final Mission",
    author="Bret Baier, Catherine Whitney",
    img="https://images-na.ssl-images-amazon.com/images/I/51oH3wddY%2BL._SX329_BO1,204,203,200_.jpg",
    category=category5)
session.add(book2)
session.commit()

book3 = Book(
    user_id=1,
    title="Hidden Figures: The American Dream and the Untold Story of the Black Women Mathematicians Who Helped Win the Space Race",
    author="Margot Lee Shetterly",
    img="https://images-na.ssl-images-amazon.com/images/I/51O1sI8z4SL._SX330_BO1,204,203,200_.jpg",
    category=category5)
session.add(book3)
session.commit()

book4 = Book(
    user_id=1,
    title="50 People Every Christian Should Know: Learning from Spiritual Giants of the Faith",
    author="Warren W. Wiersbe",
    img="https://images-na.ssl-images-amazon.com/images/I/51W%2BZf0SDtL.jpg",
    category=category5)
session.add(book4)
session.commit()

# Books for Biography
category6 = Category(name="Biography and Memoirs")
session.add(category6)
session.commit()

book1 = Book(
    user_id=1,
    title="Maude",
    author="Donna Foley Mabry",
    img="https://images-na.ssl-images-amazon.com/images/I/51i%2B8fXnPfL.jpg",
    category=category6)
session.add(book1)
session.commit()

book2 = Book(
    user_id=1,
    title="The 5 Love Languages: The Secret to Love that Lasts",
    author="Gary Chapman",
    img="https://images-na.ssl-images-amazon.com/images/I/51rV-3xwEJL._SX321_BO1,204,203,200_.jpg",
    category=category6)
session.add(book2)
session.commit()

book3 = Book(
    user_id=1,
    title="Fierce Convictions: The Extraordinary Life of Hannah More? Poet, Reformer, Abolitionist",
    author="Karen Swallow Prior",
    img="https://images-na.ssl-images-amazon.com/images/I/51szsJbYt-L.jpg",
    category=category6)
session.add(book3)
session.commit()

book4 = Book(
    user_id=1,
    title="Tears We Cannot Stop: A Sermon to White America",
    author="Michael Eric Dyson",
    img="https://images-na.ssl-images-amazon.com/images/I/51Csgg2h1bL._SX337_BO1,204,203,200_.jpg",
    category=category6)
session.add(book4)
session.commit()

# Books for Science
category7 = Category(name="Science")
session.add(category7)
session.commit()

book1 = Book(
    user_id=1,
    title="The Oyster War: The True Story of a Small Farm, Big Politics, and the Future of Wilderness in America",
    author="Summer Brennan",
    img="https://images-na.ssl-images-amazon.com/images/I/51bDDiN0H9L._SX325_BO1,204,203,200_.jpg",
    category=category7)
session.add(book1)
session.commit()

book2 = Book(
    user_id=1,
    title="Follow Your Gut: The Enormous Impact of Tiny Microbes",
    author="Rob Knight",
    img="https://images-na.ssl-images-amazon.com/images/I/51bDDiN0H9L._SX325_BO1,204,203,200_.jpg",
    category=category7)
session.add(book2)
session.commit()

book3 = Book(
    user_id=1,
    title="Subliminal: How Your Unconscious Mind Rules Your Behavior",
    author="Leonard Mlodinow",
    img="https://images-na.ssl-images-amazon.com/images/I/41X-csGlgkL._SX322_BO1,204,203,200_.jpg",
    category=category7)
session.add(book3)
session.commit()

book4 = Book(
    user_id=1,
    title="The Sweet Spot: How to Find Your Groove at Home and Work",
    author="Christine Carter Ph.D.",
    img="https://images-na.ssl-images-amazon.com/images/I/51DJc9cnjkL._SX334_BO1,204,203,200_.jpg",
    category=category7)
session.add(book4)
session.commit()

category8 = Category(name="Comics")
session.add(category8)
session.commit()

book1 = Book(
    user_id=1,
    title="March (Trilogy Slipcase Set)",
    author="John Lewis",
    img="https://images-na.ssl-images-amazon.com/images/I/51WSGTHpq6L._SX340_BO1,204,203,200_.jpg",
    category=category8)
session.add(book1)
session.commit()

book2 = Book(
    user_id=1,
    title="March: Book One",
    author="John Lewis",
    img="https://images-na.ssl-images-amazon.com/images/I/51VueibFRsL._SX326_BO1,204,203,200_.jpg",
    category=category8)
session.add(book2)
session.commit()

book3 = Book(
    user_id=1,
    title="Attack on Titan Vol. 1",
    author="Hajime Isayama",
    img="https://images-na.ssl-images-amazon.com/images/I/51QWSFImgvL.jpg",
    category=category8)
session.add(book3)
session.commit()

book4 = Book(
    user_id=1,
    title="Secret Wars (Secret Wars (2015-2016))",
    author="Jonathan Hickman",
    img="https://images-na.ssl-images-amazon.com/images/I/61ZJA9QRGKL.jpg",
    category=category8)
session.add(book4)
session.commit()


print "These are all of the categories in your database:"
categories = session.query(Category).all()
for category in categories:
    print category.name

print "These are all of the books in your database:"
books = session.query(Book).all()
for book in books:
    print book.title
