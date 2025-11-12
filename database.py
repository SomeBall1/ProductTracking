"""Database models and operations for product tracking."""
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import Config

Base = declarative_base()

class ProductCheck(Base):
    """Model for storing product availability checks."""
    __tablename__ = 'product_checks'

    id = Column(Integer, primary_key=True)
    location_name = Column(String, nullable=False)
    location_url = Column(String, nullable=False)
    product_name = Column(String, nullable=False)
    is_available = Column(Boolean, nullable=False)
    price = Column(String, nullable=True)
    checked_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ProductCheck(location='{self.location_name}', available={self.is_available}, time={self.checked_at})>"


class Database:
    """Database manager for product tracking."""

    def __init__(self):
        self.engine = create_engine(f'sqlite:///{Config.DATABASE_PATH}')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def add_check(self, location_name, location_url, product_name, is_available, price=None):
        """Add a new product check to the database."""
        check = ProductCheck(
            location_name=location_name,
            location_url=location_url,
            product_name=product_name,
            is_available=is_available,
            price=price
        )
        self.session.add(check)
        self.session.commit()
        return check

    def get_last_check(self, location_name):
        """Get the most recent check for a location."""
        return self.session.query(ProductCheck).filter_by(
            location_name=location_name
        ).order_by(ProductCheck.checked_at.desc()).first()

    def get_availability_history(self, location_name, limit=10):
        """Get recent availability history for a location."""
        return self.session.query(ProductCheck).filter_by(
            location_name=location_name
        ).order_by(ProductCheck.checked_at.desc()).limit(limit).all()

    def close(self):
        """Close the database session."""
        self.session.close()
