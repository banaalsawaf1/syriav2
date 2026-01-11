
from abc import ABC, abstractmethod

class DonationStrategy(ABC):
    """استراتيجية أساسية للتعامل مع التبرعات"""
    
    @abstractmethod
    def process_request(self, request):
        pass
    
    @abstractmethod
    def get_request_details(self):
        pass

class OrganizationDonationStrategy(DonationStrategy):
    """استراتيجية للتعامل مع طلبات المنظمات"""
    
    def __init__(self, donation_request):
        self.donation_request = donation_request
    
    def process_request(self, status):
        """معالجة طلب المنظمة (قبول/رفض)"""
        self.donation_request.status = status
        self.donation_request.save()
        
       
        if status == 'accepted':
            project = self.donation_request.project
            project.organization = self.donation_request.organization
            project.save()
    
    def get_request_details(self):
        """الحصول على تفاصيل الطلب لعرضها في الجدول"""
        return {
            'id': self.donation_request.id,
            'organization': self.donation_request.organization.username,
            'project': self.donation_request.project,
            'adoption_type': self.donation_request.get_adoption_type_display(),
            'amount': self.donation_request.amount,
            'message': self.donation_request.message,
            'created_at': self.donation_request.created_at,
            'status': self.donation_request.status,
        }

class CitizenDonationStrategy(DonationStrategy):
    """استراتيجية للتعامل مع طلبات المواطنين"""
    
    def __init__(self, donation_request):
        self.donation_request = donation_request
    
    def process_request(self, status):
        """معالجة طلب المواطن (قبول/رفض)"""
        self.donation_request.status = status
        self.donation_request.save()
    
    def get_request_details(self):
        """الحصول على تفاصيل الطلب لعرضها في الجدول"""
        return {
            'id': self.donation_request.id,
            'citizen': self.donation_request.citizen.username,
            'project': self.donation_request.project,
            'donation_amount': self.donation_request.donation_amount,
            'message': self.donation_request.message,
            'created_at': self.donation_request.created_at,
            'status': self.donation_request.status,
        }

class DonationContext:
    """السياق الذي يستخدم الاستراتيجية"""
    
    def __init__(self, strategy: DonationStrategy):
        self._strategy = strategy
    
    def set_strategy(self, strategy: DonationStrategy):
        self._strategy = strategy
    
    def process_request(self, status):
        return self._strategy.process_request(status)
    
    def get_request_details(self):
        return self._strategy.get_request_details()
