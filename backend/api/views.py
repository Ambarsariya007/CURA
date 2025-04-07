from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, ConsultationReportSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
import json
from .models import ConsultationReport

User = get_user_model()


from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from django.contrib.auth.hashers import make_password
from .serializers import UserSerializer

from django.contrib.auth import login, authenticate, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

User = get_user_model()
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User  # Import User model
from api.models import CustomUser  # Change to your custom user model if using one
from django.contrib.auth.hashers import make_password

from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print("Request Data:", request.data)  # Log the incoming data

        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        role = request.data.get("role")
        hospital = request.data.get("hospital")  # This is for doctors only

        if not username or not email or not password or not role:
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        if role == "doctor" and not hospital:
            return Response({"error": "Hospital is required for doctors"}, status=status.HTTP_400_BAD_REQUEST)

        if CustomUser.objects.filter(email=email).exists():
            return Response({"error": "Email already in use"}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            role=role,
            hospital=hospital if role == "doctor" else None  # Set hospital only for doctors
        )

        return Response({"message": "Registration successful"}, status=status.HTTP_201_CREATED)



class CSRFTokenView(APIView):
    def get(self, request):
        return Response({"csrftoken": get_token(request)})
# class LoginView(APIView):
#     def post(self, request):
#         print("Incoming Login Data:", request.data)  # ✅ Debugging

#         email = request.data.get("email")
#         password = request.data.get("password")

#         if not email or not password:
#             print("❌ Missing email or password")
#             return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             user = User.objects.get(email=email)
#             print(f"✅ Found user: {user.email}")  # ✅ Debug user lookup
#         except User.DoesNotExist:
#             print("❌ User not found")
#             return Response({"error": "User not found."}, status=status.HTTP_400_BAD_REQUEST)

#         user = authenticate(request=request, username=email, password=password)

#         if user is not None:
#             print("✅ Authentication successful")
#             return Response({"message": "Login successful!"}, status=status.HTTP_200_OK)

#         print("❌ Invalid credentials")
#         return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password

User = get_user_model()  # ✅ Get custom user model

class LoginView(APIView):
    authentication_classes = []  # ✅ No authentication required for login
    permission_classes = [AllowAny]  # ✅ Allow all users to access

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        # ✅ Get user by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Invalid email or password"}, status=400)

        # ✅ Check password manually
        if not check_password(password, user.password):
            return Response({"error": "Invalid email or password"}, status=400)

        # ✅ Generate or retrieve the token
        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            "user": {
                "id": user.id,
                "name": user.username,  # Use .first_name if needed
                "email": user.email
            }
        })

from django.contrib.auth import logout
from django.http import JsonResponse

from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt

def csrf_token_view(request):
    token = get_token(request)
    return JsonResponse({"csrfToken": token})  # ✅ Sends CSRF token to frontend

@csrf_exempt  # 🚨 Debugging only, remove later
def logout_view(request):
    if request.method == "POST":
        logout(request)
        response = JsonResponse({"message": "Logged out successfully"})
        response.delete_cookie("sessionid")  # ✅ Ensure session is cleared
        return response
    return JsonResponse({"error": "Invalid request"}, status=400)



    
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        response = Response(serializer.data, status=status.HTTP_200_OK)
        response["Access-Control-Allow-Credentials"] = "true"
        return response
class CheckAuthView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return Response({
                "authenticated": True,
                "user": {
                    "id": request.user.id,
                    "email": request.user.email
                }
            }, status=status.HTTP_200_OK)
        return Response({"authenticated": False}, status=status.HTTP_200_OK)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import logout

class LogoutView(APIView):
    def post(self, request):
        # Perform logout
        logout(request)
        
        # Clear session data
        request.session.flush()
        
        return Response({"success": True, "message": "Logout successful"}, status=status.HTTP_200_OK)

    

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from django.contrib.auth.decorators import login_required

@login_required
def get_user(request):
    if request.user.is_authenticated:
        return JsonResponse({"username": request.user.username})
    return JsonResponse({"error": "User not authenticated"}, status=401)

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse

def get_user_data(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "User not authenticated"}, status=401)
    
    user = request.user
    return JsonResponse({
        "username": user.username,
        "email": user.email
    })

from django.contrib.auth import logout
from django.http import JsonResponse

def logout_view(request):
    logout(request)
    return JsonResponse({"message": "Logged out successfully"}, status=200)

from .models import ConsultationReport

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ConsultationReport

import logging

import json
import logging
from django.http import JsonResponse
from .models import ConsultationReport
from django.views.decorators.csrf import csrf_exempt

def save_consultation(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            logging.info(f"Received data: {data}")  # Log received data for debugging

            user_id = data.get("user_id", None)
            responses = data.get("responses", {})
            ml_result = data.get("mlResult", "Not Available")

            # Additional validation logs
            logging.info(f"User ID: {user_id}")
            logging.info(f"Responses: {responses}")
            logging.info(f"ML Result: {ml_result}")

            # Save data in the database
            report = ConsultationReport.objects.create(
                user_id=user_id,
                responses=responses,
                ml_result=ml_result
            )

            return JsonResponse({"message": "Consultation saved successfully!", "report_id": report.id}, status=201)

        except Exception as e:
            logging.error(f"Error saving consultation: {str(e)}")
            return JsonResponse({"error": str(e)}, status=400)



from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import json
from .models import ConsultationReport

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from .models import ConsultationReport

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from django.http import HttpResponse
from .models import ConsultationReport

def generate_pdf(request, report_id):
    try:
        # Fetch the report data from the database
        report = ConsultationReport.objects.get(id=report_id)

        # Create an HTTP response with a PDF file
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="consultation_report_{report_id}.pdf"'

        # Define modern color scheme
        primary_color = colors.HexColor('#1E88E5')  # Modern blue
        secondary_color = colors.HexColor('#43A047')  # Modern green
        text_color = colors.HexColor('#212121')  # Near black
        light_bg = colors.HexColor('#F5F5F5')  # Very light gray

        # Create PDF document with margins
        doc = SimpleDocTemplate(
            response, 
            pagesize=letter,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch,
            leftMargin=0.75*inch,
            rightMargin=0.75*inch
        )
        
        elements = []
        styles = getSampleStyleSheet()

        # Create custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=24,
            textColor=primary_color,
            spaceAfter=16,
            alignment=1  # Center alignment
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading2'],
            fontSize=18,
            textColor=secondary_color,
            spaceAfter=12
        )
        
        # Modified section_title style to ensure it's not italicized
        section_title = ParagraphStyle(
            'SectionTitle',
            parent=styles['Heading3'],
            fontSize=14,
            textColor=text_color,
            spaceBefore=12,
            spaceAfter=6,
            fontName='Helvetica-Bold',  # Using regular bold font instead of potentially italic
            italic=0  # Explicitly setting italic to 0 (off)
        )
        
        body_text = ParagraphStyle(
            'BodyText',
            parent=styles['Normal'],
            fontSize=10,
            textColor=text_color,
            leading=14
        )

        # Header with modern styling
        cura_header = Paragraph(
            "<font color='#1E88E5'><b>CURA</b></font> <font color='#43A047'>Health Consultation</font>",
            title_style
        )
        elements.append(cura_header)
        
        # Report subtitle
        report_title = Paragraph(
            f"Consultation Report #{report.id}",
            subtitle_style
        )
        elements.append(report_title)
        
        # Date & time info
        if hasattr(report, 'created_at'):
            date_info = Paragraph(
                f"Generated on: {report.created_at.strftime('%B %d, %Y at %H:%M')}",
                body_text
            )
            elements.append(date_info)
        
        elements.append(Spacer(1, 20))
        
        # Horizontal separator
        separator_style = TableStyle([
            ('LINEBELOW', (0, 0), (-1, 0), 1, primary_color),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 0),
        ])
        separator = Table([['']],  colWidths=[7*inch])
        separator.setStyle(separator_style)
        elements.append(separator)
        elements.append(Spacer(1, 20))

        # Basic Information Section with modern table - non-italicized section title
        elements.append(Paragraph("Report Summary", section_title))
        elements.append(Spacer(1, 6))
        try:
            ml_data = json.loads(report.ml_result)
            predicted_diseases = ml_data.get("predicted_diseases", []) # Top 3
            top_disease_names = ", ".join(d["disease"] for d in predicted_diseases)
        except Exception:
            top_disease_names = "N/A"

        user_info = [
            [Paragraph("<b>Report ID:</b>", body_text), Paragraph(str(report.id), body_text)],
            [Paragraph("<b>ML Diagnosis:</b>", body_text), Paragraph(top_disease_names, body_text)],
        ]


        # Modern table with clean styling
        table = Table(user_info, colWidths=[2*inch, 4.5*inch])
        table.setStyle(TableStyle([ 
            # Headers
            ('BACKGROUND', (0, 0), (0, -1), light_bg),
            ('TEXTCOLOR', (0, 0), (0, -1), text_color),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            # Content
            ('BACKGROUND', (1, 0), (1, -1), colors.white),
            # Border styling
            ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
            # Padding
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 30))

        # User Responses Section with modern styling - non-italicized section title
        if report.responses:
            elements.append(Paragraph("Consultation Responses", section_title))
            elements.append(Spacer(1, 6))
            
            # Create enhanced header row
            response_data = [
                [Paragraph("<b>Question</b>", body_text), 
                 Paragraph("<b>Response</b>", body_text)]
            ]
            
            # Add each Q&A row with enhanced styling
            for q, a in report.responses.items():
                question_text = Paragraph(q, body_text)
                answer_text = Paragraph(a, body_text)
                response_data.append([question_text, answer_text])

            response_table = Table(response_data, colWidths=[3.25*inch, 3.25*inch])
            
            # Create dynamic alternating row styles
            table_style = [
                # Header styling
                ('BACKGROUND', (0, 0), (-1, 0), primary_color),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                # Grid styling
                ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
                # Padding
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('LEFTPADDING', (0, 0), (-1, -1), 12),
                ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ]
            
            # Add alternating row colors dynamically based on available rows
            for i in range(1, len(response_data)):
                if i % 2 == 0:  # Even rows (starting from 1-based index)
                    table_style.append(('BACKGROUND', (0, i), (-1, i), light_bg))
                else:  # Odd rows
                    table_style.append(('BACKGROUND', (0, i), (-1, i), colors.white))
            
            response_table.setStyle(TableStyle(table_style))
            elements.append(response_table)
            elements.append(Spacer(1, 30))

        # Add disclaimer
        disclaimer_style = ParagraphStyle(
            'Disclaimer',
            parent=styles['Italic'],
            fontSize=8,
            textColor=colors.grey,
            alignment=1  # Center alignment
        )
        disclaimer = Paragraph(
            "This report is computer-generated and may require review by a healthcare professional. "
            "CURA's ML diagnosis is not a substitute for professional medical advice.",
            disclaimer_style
        )
        elements.append(disclaimer)
        elements.append(Spacer(1, 12))
        
        # Modern footer with separator
        footer_separator = Table([['']],  colWidths=[7*inch])
        footer_separator.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (-1, 0), 0.5, colors.lightgrey),
            ('TOPPADDING', (0, 0), (-1, 0), 0),
        ]))
        elements.append(footer_separator)
        
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=9,
            textColor=secondary_color,
            alignment=1  # Center alignment
        )
        footer = Paragraph(
            "Thank you for using <b>CURA</b> Health Consultation Platform | Stay Healthy",
            footer_style
        )
        elements.append(Spacer(1, 8))
        elements.append(footer)

        # Build the PDF
        doc.build(elements)
        return response

    except ConsultationReport.DoesNotExist:
        return HttpResponse("Report not found", status=404)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)


import torch
import numpy as np
import pandas as pd
from torch import nn
# Load indexes (Manually copy the dictionary from your dataset)
disease_indexes = {'Fungal infection': 0, 'Allergy': 1, 'GERD': 2, 'Chronic cholestasis': 3, 'Drug Reaction': 4,
                   'Peptic ulcer diseae': 5, 'AIDS': 6, 'Diabetes ': 7, 'Gastroenteritis': 8, 'Bronchial Asthma': 9,
                   'Hypertension ': 10, 'Migraine': 11, 'Cervical spondylosis': 12, 'Paralysis (brain hemorrhage)': 13,
                   'Jaundice': 14, 'Malaria': 15, 'Chicken pox': 16, 'Dengue': 17, 'Typhoid': 18, 'hepatitis A': 19,
                   'Hepatitis B': 20, 'Hepatitis C': 21, 'Hepatitis D': 22, 'Hepatitis E': 23, 'Alcoholic hepatitis': 24,
                   'Tuberculosis': 25, 'Common Cold': 26, 'Pneumonia': 27, 'Dimorphic hemmorhoids(piles)': 28, 'Heart attack': 29,
                   'Varicose veins': 30, 'Hypothyroidism': 31, 'Hyperthyroidism': 32, 'Hypoglycemia': 33, 'Osteoarthristis': 34,
                   'Arthritis': 35, '(vertigo) Paroymsal  Positional Vertigo': 36, 'Acne': 37, 'Urinary tract infection': 38,
                   'Psoriasis': 39, 'Impetigo': 40}

symptom_indexes = {' abdominal_pain': 0, ' abnormal_menstruation': 1, ' acidity': 2, ' acute_liver_failure': 3, ' altered_sensorium': 4, ' anxiety': 5, ' back_pain': 6, ' belly_pain': 7, ' blackheads': 8, ' bladder_discomfort': 9, ' blister': 10, ' blood_in_sputum': 11, ' bloody_stool': 12, ' blurred_and_distorted_vision': 13, ' breathlessness': 14, ' brittle_nails': 15, ' bruising': 16, ' burning_micturition': 17, ' chest_pain': 18, ' chills': 19, ' cold_hands_and_feets': 20, ' coma': 21, ' congestion': 22, ' constipation': 23, ' continuous_feel_of_urine': 24, ' continuous_sneezing': 25, ' cough': 26, ' cramps': 27, ' dark_urine': 28, ' dehydration': 29, ' depression': 30, ' diarrhoea': 31, ' dischromic patches': 32, ' distention_of_abdomen': 33, ' dizziness': 34, ' drying_and_tingling_lips': 35, ' enlarged_thyroid': 36, ' excessive_hunger': 37, ' extra_marital_contacts': 38, ' family_history': 39, ' fast_heart_rate': 40, ' fatigue': 41, ' fluid_overload': 42, ' foul_smell_of urine': 43, ' headache': 44, ' high_fever': 45, ' hip_joint_pain': 46, ' history_of_alcohol_consumption': 47, ' increased_appetite': 48, ' indigestion': 49, ' inflammatory_nails': 50, ' internal_itching': 51, ' irregular_sugar_level': 52, ' irritability': 53, ' irritation_in_anus': 54, ' joint_pain': 55, ' knee_pain': 56, ' lack_of_concentration': 57, ' lethargy': 58, ' loss_of_appetite': 59, ' loss_of_balance': 60, ' loss_of_smell': 61, ' malaise': 62, ' mild_fever': 63, ' mood_swings': 64, ' movement_stiffness': 65, ' mucoid_sputum': 66, ' muscle_pain': 67, ' muscle_wasting': 68, ' muscle_weakness': 69, ' nausea': 70, ' neck_pain': 71, ' nodal_skin_eruptions': 72, ' obesity': 73, ' pain_behind_the_eyes': 74, ' pain_during_bowel_movements': 75, ' pain_in_anal_region': 76, ' painful_walking': 77, ' palpitations': 78, ' passage_of_gases': 79, ' patches_in_throat': 80, ' phlegm': 81, ' polyuria': 82, ' prominent_veins_on_calf': 83, ' puffy_face_and_eyes': 84, ' pus_filled_pimples': 85, ' receiving_blood_transfusion': 86, ' receiving_unsterile_injections': 87, ' red_sore_around_nose': 88, ' red_spots_over_body': 89, ' redness_of_eyes': 90, ' restlessness': 91, ' runny_nose': 92, ' rusty_sputum': 93, ' scurring': 94, ' shivering': 95, ' silver_like_dusting': 96, ' sinus_pressure': 97, ' skin_peeling': 98, ' skin_rash': 99, ' slurred_speech': 100, ' small_dents_in_nails': 101, ' spinning_movements': 102, ' spotting urination': 103, ' stiff_neck': 104, ' stomach_bleeding': 105, ' stomach_pain': 106, ' sunken_eyes': 107, ' sweating': 108, ' swelled_lymph_nodes': 109, ' swelling_joints': 110, ' swelling_of_stomach': 111, ' swollen_blood_vessels': 112, ' swollen_extremeties': 113, ' swollen_legs': 114, ' throat_irritation': 115, ' toxic_look_(typhos)': 116, ' ulcers_on_tongue': 117, ' unsteadiness': 118, ' visual_disturbances': 119, ' vomiting': 120, ' watering_from_eyes': 121, ' weakness_in_limbs': 122, ' weakness_of_one_body_side': 123, ' weight_gain': 124, ' weight_loss': 125, ' yellow_crust_ooze': 126, ' yellow_urine': 127, ' yellowing_of_eyes': 128, ' yellowish_skin': 129, '(vertigo) Paroymsal  Positional Vertigo': 130, 'AIDS': 131, 'Acne': 132, 'Alcoholic hepatitis': 133, 'Allergy': 134, 'Arthritis': 135, 'Bronchial Asthma': 136, 'Cervical spondylosis': 137, 'Chicken pox': 138, 'Chronic cholestasis': 139, 'Common Cold': 140, 'Dengue': 141, 'Diabetes ': 142, 'Dimorphic hemmorhoids(piles)': 143, 'Drug Reaction': 144, 'Fungal infection': 145, 'GERD': 146, 'Gastroenteritis': 147, 'Heart attack': 148, 'Hepatitis B': 149, 'Hepatitis C': 150, 'Hepatitis D': 151, 'Hepatitis E': 152, 'Hypertension ': 153, 'Hyperthyroidism': 154, 'Hypoglycemia': 155, 'Hypothyroidism': 156, 'Impetigo': 157, 'Jaundice': 158, 'Malaria': 159, 'Migraine': 160, 'Osteoarthristis': 161, 'Paralysis (brain hemorrhage)': 162, 'Peptic ulcer diseae': 163, 'Pneumonia': 164, 'Psoriasis': 165, 'Tuberculosis': 166, 'Typhoid': 167, 'Urinary tract infection': 168, 'Varicose veins': 169, 'hepatitis A': 170, 'itching': 171}

# Load trained model
import torch.nn as nn

class SymptomClassifier(nn.Module):
    def __init__(self, input_size: int, num_classes: int):  # <-- fix here
        super().__init__()  # <-- and here
        self.model = nn.Sequential(
            nn.Linear(in_features=input_size, out_features=128),
            nn.ReLU(),
            nn.Linear(in_features=128, out_features=64),
            nn.Tanh(),
            nn.Linear(in_features=64, out_features=num_classes)
        )
        
    def forward(self, input):
        return self.model(input)
    
# Initialize Model
input_size = len(symptom_indexes)
num_classes = len(disease_indexes)
classifier = SymptomClassifier(input_size, num_classes)

# Load model weights
classifier.load_state_dict(torch.load("bhsoda.pth"))
classifier.eval()

# Function to predict disease from symptoms
def predict_disease(symptom_indexes_list, top_k=3):
    # Create symptom vector
    input_vector = np.zeros(len(symptom_indexes))  # Initialize all symptoms as 0
    associated_symptoms = []  # Store actual symptom names

    for idx in symptom_indexes_list:
        if 0 <= idx < len(symptom_indexes):  # Ensure the index is valid
            input_vector[idx] = 1
            symptom_name = list(symptom_indexes.keys())[list(symptom_indexes.values()).index(idx)]
            associated_symptoms.append(symptom_name)
        else:
            print(f"Warning: Symptom index '{idx}' is out of range.")

    # Convert to tensor
    input_tensor = torch.Tensor(input_vector).unsqueeze(0)  # Add batch dimension
    
    # Make prediction
    with torch.no_grad():
        output = classifier(input_tensor)  # Get raw logits
        probabilities = torch.softmax(output, dim=-1)  # Convert logits to probabilities
        top_probs, top_indices = torch.topk(probabilities, top_k, dim=-1)  # Get top-k predictions
    
    # Extract top-k predictions
    top_probs = top_probs.squeeze().tolist()  # Convert tensor to list
    top_indices = top_indices.squeeze().tolist()  # Convert tensor to list

    # Map indices to disease names
    top_diseases = [(list(disease_indexes.keys())[list(disease_indexes.values()).index(idx)], prob * 100) 
                    for idx, prob in zip(top_indices, top_probs)]

    # Print the associated symptoms
    '''
    print("Symptoms Associated with Input:")
    for symptom in associated_symptoms:
        print(f"- {symptom}")

    print("\nTop Predicted Diseases:")
    for disease, prob in top_diseases:
        print(f"{disease}")
    '''
    
    finalstring = str(associated_symptoms) + "\n" + str(top_diseases)
    reccomendation = reccomender.generate_reccomendation(finalstring)
    return reccomendation
    





import google.generativeai as genai
import re
import json

# Secure API Key (Store in Environment Variables Instead)
genai.configure(api_key="AIzaSyASjCwVvZUCK6WdC03nQm-1pM8aSAy5WCo")

model = genai.GenerativeModel('gemini-1.5-flash')

context = {' abdominal_pain': 0, ' abnormal_menstruation': 1, ' acidity': 2, ' acute_liver_failure': 3, ' altered_sensorium': 4, ' anxiety': 5, ' back_pain': 6, ' belly_pain': 7, ' blackheads': 8, ' bladder_discomfort': 9, ' blister': 10, ' blood_in_sputum': 11, ' bloody_stool': 12, ' blurred_and_distorted_vision': 13, ' breathlessness': 14, ' brittle_nails': 15, ' bruising': 16, ' burning_micturition': 17, ' chest_pain': 18, ' chills': 19, ' cold_hands_and_feets': 20, ' coma': 21, ' congestion': 22, ' constipation': 23, ' continuous_feel_of_urine': 24, ' continuous_sneezing': 25, ' cough': 26, ' cramps': 27, ' dark_urine': 28, ' dehydration': 29, ' depression': 30, ' diarrhoea': 31, ' dischromic patches': 32, ' distention_of_abdomen': 33, ' dizziness': 34, ' drying_and_tingling_lips': 35, ' enlarged_thyroid': 36, ' excessive_hunger': 37, ' extra_marital_contacts': 38, ' family_history': 39, ' fast_heart_rate': 40, ' fatigue': 41, ' fluid_overload': 42, ' foul_smell_of urine': 43, ' headache': 44, ' high_fever': 45, ' hip_joint_pain': 46, ' history_of_alcohol_consumption': 47, ' increased_appetite': 48, ' indigestion': 49, ' inflammatory_nails': 50, ' internal_itching': 51, ' irregular_sugar_level': 52, ' irritability': 53, ' irritation_in_anus': 54, ' joint_pain': 55, ' knee_pain': 56, ' lack_of_concentration': 57, ' lethargy': 58, ' loss_of_appetite': 59, ' loss_of_balance': 60, ' loss_of_smell': 61, ' malaise': 62, ' mild_fever': 63, ' mood_swings': 64, ' movement_stiffness': 65, ' mucoid_sputum': 66, ' muscle_pain': 67, ' muscle_wasting': 68, ' muscle_weakness': 69, ' nausea': 70, ' neck_pain': 71, ' nodal_skin_eruptions': 72, ' obesity': 73, ' pain_behind_the_eyes': 74, ' pain_during_bowel_movements': 75, ' pain_in_anal_region': 76, ' painful_walking': 77, ' palpitations': 78, ' passage_of_gases': 79, ' patches_in_throat': 80, ' phlegm': 81, ' polyuria': 82, ' prominent_veins_on_calf': 83, ' puffy_face_and_eyes': 84, ' pus_filled_pimples': 85, ' receiving_blood_transfusion': 86, ' receiving_unsterile_injections': 87, ' red_sore_around_nose': 88, ' red_spots_over_body': 89, ' redness_of_eyes': 90, ' restlessness': 91, ' runny_nose': 92, ' rusty_sputum': 93, ' scurring': 94, ' shivering': 95, ' silver_like_dusting': 96, ' sinus_pressure': 97, ' skin_peeling': 98, ' skin_rash': 99, ' slurred_speech': 100, ' small_dents_in_nails': 101, ' spinning_movements': 102, ' spotting urination': 103, ' stiff_neck': 104, ' stomach_bleeding': 105, ' stomach_pain': 106, ' sunken_eyes': 107, ' sweating': 108, ' swelled_lymph_nodes': 109, ' swelling_joints': 110, ' swelling_of_stomach': 111, ' swollen_blood_vessels': 112, ' swollen_extremeties': 113, ' swollen_legs': 114, ' throat_irritation': 115, ' toxic_look_(typhos)': 116, ' ulcers_on_tongue': 117, ' unsteadiness': 118, ' visual_disturbances': 119, ' vomiting': 120, ' watering_from_eyes': 121, ' weakness_in_limbs': 122, ' weakness_of_one_body_side': 123, ' weight_gain': 124, ' weight_loss': 125, ' yellow_crust_ooze': 126, ' yellow_urine': 127, ' yellowing_of_eyes': 128, ' yellowish_skin': 129, '(vertigo) Paroymsal  Positional Vertigo': 130, 'AIDS': 131, 'Acne': 132, 'Alcoholic hepatitis': 133, 'Allergy': 134, 'Arthritis': 135, 'Bronchial Asthma': 136, 'Cervical spondylosis': 137, 'Chicken pox': 138, 'Chronic cholestasis': 139, 'Common Cold': 140, 'Dengue': 141, 'Diabetes ': 142, 'Dimorphic hemmorhoids(piles)': 143, 'Drug Reaction': 144, 'Fungal infection': 145, 'GERD': 146, 'Gastroenteritis': 147, 'Heart attack': 148, 'Hepatitis B': 149, 'Hepatitis C': 150, 'Hepatitis D': 151, 'Hepatitis E': 152, 'Hypertension ': 153, 'Hyperthyroidism': 154, 'Hypoglycemia': 155, 'Hypothyroidism': 156, 'Impetigo': 157, 'Jaundice': 158, 'Malaria': 159, 'Migraine': 160, 'Osteoarthristis': 161, 'Paralysis (brain hemorrhage)': 162, 'Peptic ulcer diseae': 163, 'Pneumonia': 164, 'Psoriasis': 165, 'Tuberculosis': 166, 'Typhoid': 167, 'Urinary tract infection': 168, 'Varicose veins': 169, 'hepatitis A': 170, 'itching': 171}
context_string = "\n".join([f"{key}: {value}" for key, value in context.items()])

def generate_reccomendation(user_text):
    prompt = f"""
    You are given the following symptoms and predicted diseases:
    {user_text}
    
    return the type/types of doctors that would be the most beneficial in this case, could be 1-3 types depending on how broad the symptoms are
    
    i want you to return the following in json: 
    every symptom, every predicted disease, and type of doctor, no explanation needed, strictly in json"
    """

    response = model.generate_content(prompt)
    json_match = re.search(r'\{.*\}', response.text.strip(), re.DOTALL)

    if json_match:
        json_text = json_match.group(0)  # Extract matched JSON content
        try:
            cleaned_json = json.loads(json_text)  # Validate and parse JSON
            json_string = json.dumps(cleaned_json)  # Convert back to JSON string
        except json.JSONDecodeError:
            json_string = None  # Handle invalid JSON case
    else:
        json_string = None  # No JSON found
    
    return json_string


# Initialize Model
input_size = len(symptom_indexes)
num_classes = len(disease_indexes)
classifier = SymptomClassifier(input_size, num_classes)

# Load model weights
classifier.load_state_dict(torch.load("bhsoda.pth"))
classifier.eval()

# Function to predict disease from symptoms
def predict_disease(symptom_indexes_list, top_k=3):
    # Create symptom vector
    input_vector = np.zeros(len(symptom_indexes))  # Initialize all symptoms as 0
    associated_symptoms = []  # Store actual symptom names

    for idx in symptom_indexes_list:
        if 0 <= idx < len(symptom_indexes):  # Ensure the index is valid
            input_vector[idx] = 1
            symptom_name = list(symptom_indexes.keys())[list(symptom_indexes.values()).index(idx)]
            associated_symptoms.append(symptom_name)
        else:
            print(f"Warning: Symptom index '{idx}' is out of range.")

    # Convert to tensor
    input_tensor = torch.Tensor(input_vector).unsqueeze(0)  # Add batch dimension
    
    # Make prediction
    with torch.no_grad():
        output = classifier(input_tensor)  # Get raw logits
        probabilities = torch.softmax(output, dim=-1)  # Convert logits to probabilities
        top_probs, top_indices = torch.topk(probabilities, top_k, dim=-1)  # Get top-k predictions
    
    # Extract top-k predictions
    top_probs = top_probs.squeeze().tolist()  # Convert tensor to list
    top_indices = top_indices.squeeze().tolist()  # Convert tensor to list

    # Map indices to disease names
    top_diseases = [(list(disease_indexes.keys())[list(disease_indexes.values()).index(idx)], prob * 100) 
                    for idx, prob in zip(top_indices, top_probs)]

    # Print the associated symptoms
    '''
    print("Symptoms Associated with Input:")
    for symptom in associated_symptoms:
        print(f"- {symptom}")

    print("\nTop Predicted Diseases:")
    for disease, prob in top_diseases:
        print(f"{disease}")
    '''
    
    finalstring = str(associated_symptoms) + "\n" + str(top_diseases)
    reccomendation = generate_reccomendation(finalstring)
    return reccomendation





import google.generativeai as genai
import ast

# Secure API Key (Store in Environment Variables Instead)
genai.configure(api_key="AIzaSyASjCwVvZUCK6WdC03nQm-1pM8aSAy5WCo")

model = genai.GenerativeModel('gemini-1.5-flash')

context = {' abdominal_pain': 0, ' abnormal_menstruation': 1, ' acidity': 2, ' acute_liver_failure': 3, ' altered_sensorium': 4, ' anxiety': 5, ' back_pain': 6, ' belly_pain': 7, ' blackheads': 8, ' bladder_discomfort': 9, ' blister': 10, ' blood_in_sputum': 11, ' bloody_stool': 12, ' blurred_and_distorted_vision': 13, ' breathlessness': 14, ' brittle_nails': 15, ' bruising': 16, ' burning_micturition': 17, ' chest_pain': 18, ' chills': 19, ' cold_hands_and_feets': 20, ' coma': 21, ' congestion': 22, ' constipation': 23, ' continuous_feel_of_urine': 24, ' continuous_sneezing': 25, ' cough': 26, ' cramps': 27, ' dark_urine': 28, ' dehydration': 29, ' depression': 30, ' diarrhoea': 31, ' dischromic patches': 32, ' distention_of_abdomen': 33, ' dizziness': 34, ' drying_and_tingling_lips': 35, ' enlarged_thyroid': 36, ' excessive_hunger': 37, ' extra_marital_contacts': 38, ' family_history': 39, ' fast_heart_rate': 40, ' fatigue': 41, ' fluid_overload': 42, ' foul_smell_of urine': 43, ' headache': 44, ' high_fever': 45, ' hip_joint_pain': 46, ' history_of_alcohol_consumption': 47, ' increased_appetite': 48, ' indigestion': 49, ' inflammatory_nails': 50, ' internal_itching': 51, ' irregular_sugar_level': 52, ' irritability': 53, ' irritation_in_anus': 54, ' joint_pain': 55, ' knee_pain': 56, ' lack_of_concentration': 57, ' lethargy': 58, ' loss_of_appetite': 59, ' loss_of_balance': 60, ' loss_of_smell': 61, ' malaise': 62, ' mild_fever': 63, ' mood_swings': 64, ' movement_stiffness': 65, ' mucoid_sputum': 66, ' muscle_pain': 67, ' muscle_wasting': 68, ' muscle_weakness': 69, ' nausea': 70, ' neck_pain': 71, ' nodal_skin_eruptions': 72, ' obesity': 73, ' pain_behind_the_eyes': 74, ' pain_during_bowel_movements': 75, ' pain_in_anal_region': 76, ' painful_walking': 77, ' palpitations': 78, ' passage_of_gases': 79, ' patches_in_throat': 80, ' phlegm': 81, ' polyuria': 82, ' prominent_veins_on_calf': 83, ' puffy_face_and_eyes': 84, ' pus_filled_pimples': 85, ' receiving_blood_transfusion': 86, ' receiving_unsterile_injections': 87, ' red_sore_around_nose': 88, ' red_spots_over_body': 89, ' redness_of_eyes': 90, ' restlessness': 91, ' runny_nose': 92, ' rusty_sputum': 93, ' scurring': 94, ' shivering': 95, ' silver_like_dusting': 96, ' sinus_pressure': 97, ' skin_peeling': 98, ' skin_rash': 99, ' slurred_speech': 100, ' small_dents_in_nails': 101, ' spinning_movements': 102, ' spotting urination': 103, ' stiff_neck': 104, ' stomach_bleeding': 105, ' stomach_pain': 106, ' sunken_eyes': 107, ' sweating': 108, ' swelled_lymph_nodes': 109, ' swelling_joints': 110, ' swelling_of_stomach': 111, ' swollen_blood_vessels': 112, ' swollen_extremeties': 113, ' swollen_legs': 114, ' throat_irritation': 115, ' toxic_look_(typhos)': 116, ' ulcers_on_tongue': 117, ' unsteadiness': 118, ' visual_disturbances': 119, ' vomiting': 120, ' watering_from_eyes': 121, ' weakness_in_limbs': 122, ' weakness_of_one_body_side': 123, ' weight_gain': 124, ' weight_loss': 125, ' yellow_crust_ooze': 126, ' yellow_urine': 127, ' yellowing_of_eyes': 128, ' yellowish_skin': 129, '(vertigo) Paroymsal  Positional Vertigo': 130, 'AIDS': 131, 'Acne': 132, 'Alcoholic hepatitis': 133, 'Allergy': 134, 'Arthritis': 135, 'Bronchial Asthma': 136, 'Cervical spondylosis': 137, 'Chicken pox': 138, 'Chronic cholestasis': 139, 'Common Cold': 140, 'Dengue': 141, 'Diabetes ': 142, 'Dimorphic hemmorhoids(piles)': 143, 'Drug Reaction': 144, 'Fungal infection': 145, 'GERD': 146, 'Gastroenteritis': 147, 'Heart attack': 148, 'Hepatitis B': 149, 'Hepatitis C': 150, 'Hepatitis D': 151, 'Hepatitis E': 152, 'Hypertension ': 153, 'Hyperthyroidism': 154, 'Hypoglycemia': 155, 'Hypothyroidism': 156, 'Impetigo': 157, 'Jaundice': 158, 'Malaria': 159, 'Migraine': 160, 'Osteoarthristis': 161, 'Paralysis (brain hemorrhage)': 162, 'Peptic ulcer diseae': 163, 'Pneumonia': 164, 'Psoriasis': 165, 'Tuberculosis': 166, 'Typhoid': 167, 'Urinary tract infection': 168, 'Varicose veins': 169, 'hepatitis A': 170, 'itching': 171}
context_string = "\n".join([f"{key}: {value}" for key, value in context.items()])

def generate_symptoms(user_text):
    prompt = f"""
    You are given the following symptom dictionary:
    {context_string}
    
    The user will describe their symptoms. Your task is to return a Python list containing only the key numbers of the symptoms that match the user's input.
    
    Respond ONLY with a valid Python list of numbers and nothing else.

    User input: "{user_text}"
    """

    response = model.generate_content(prompt)

    try:
        key_numbers = ast.literal_eval(response.text.strip())
        if isinstance(key_numbers, list) and all(isinstance(i, int) for i in key_numbers):
            return key_numbers
    except (SyntaxError, ValueError):
        return []

# Example input
user_input = "i have acidity, stomach pain and im tired all the time"
symptom_keys = generate_symptoms(user_input)
final_output = predict_disease(symptom_keys)
print(final_output)


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import ast

# Assuming you already imported your model and context_string
# And imported generate_symptoms, predict_disease

@csrf_exempt
def predict_disease_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_text = data.get("complaint", "")

            if not user_text:
                return JsonResponse({"error": "No complaint text provided."}, status=400)

            symptom_keys = generate_symptoms(user_text)
            predicted_condition = predict_disease(symptom_keys)

            return JsonResponse({
                "predicted_condition": predicted_condition,
                "symptom_keys": symptom_keys
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)