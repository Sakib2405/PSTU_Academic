@echo off
cd "E:\Flutter project\medicore\lib"

:: Create folders
mkdir constants models providers services screens widgets utils config extensions
mkdir screens\core screens\patient screens\doctor screens\admin screens\patient\store
mkdir widgets\common widgets\patient widgets\doctor widgets\admin widgets\patient\store

:: Core files
type nul > main.dart
type nul > firebase_options.dart
type nul > app.dart

:: Constants
type nul > constants\colors.dart
type nul > constants\strings.dart
type nul > constants\assets.dart

:: Models
type nul > models\user_model.dart
type nul > models\doctor_model.dart
type nul > models\appointment_model.dart
type nul > models\prescription_model.dart
type nul > models\payment_model.dart
type nul > models\medicine_model.dart
type nul > models\analysis_model.dart
type nul > models\cart_item_model.dart

:: Providers
type nul > providers\auth_provider.dart
type nul > providers\doctor_provider.dart
type nul > providers\appointment_provider.dart
type nul > providers\prescription_provider.dart
type nul > providers\order_provider.dart
type nul > providers\ai_provider.dart
type nul > providers\cart_provider.dart

:: Services
type nul > services\auth_service.dart
type nul > services\doctor_service.dart
type nul > services\appointment_service.dart
type nul > services\prescription_service.dart
type nul > services\payment_service.dart
type nul > services\order_service.dart
type nul > services\ai_service.dart
type nul > services\notification_service.dart
type nul > services\store_service.dart

:: Screens - Core
type nul > screens\core\splash_screen.dart
type nul > screens\core\login_screen.dart
type nul > screens\core\signup_screen.dart
type nul > screens\core\verification_screen.dart
type nul > screens\core\settings_screen.dart
type nul > screens\core\notifications_screen.dart

:: Screens - Patient
type nul > screens\patient\patient_home_screen.dart
type nul > screens\patient\doctor_list_screen.dart
type nul > screens\patient\appointment_booking_screen.dart
type nul > screens\patient\my_appointments_screen.dart
type nul > screens\patient\appointment_detail_screen.dart
type nul > screens\patient\medical_records_screen.dart
type nul > screens\patient\order_screen.dart
type nul > screens\patient\profile_screen.dart
type nul > screens\patient\symptom_checker_screen.dart

:: Screens - Store
type nul > screens\patient\store\medicine_store_screen.dart
type nul > screens\patient\store\medicine_detail_screen.dart
type nul > screens\patient\store\cart_screen.dart
type nul > screens\patient\store\checkout_screen.dart

:: Screens - Doctor
type nul > screens\doctor\doctor_home_screen.dart
type nul > screens\doctor\pending_appointments_screen.dart
type nul > screens\doctor\patient_history_screen.dart
type nul > screens\doctor\e_prescription_screen.dart
type nul > screens\doctor\doctor_profile_screen.dart

:: Screens - Admin
type nul > screens\admin\admin_home_screen.dart
type nul > screens\admin\manage_users_screen.dart
type nul > screens\admin\manage_doctors_screen.dart
type nul > screens\admin\manage_orders_screen.dart
type nul > screens\admin\manage_appointments_screen.dart
type nul > screens\admin\manage_store_screen.dart

:: Widgets - Common
type nul > widgets\common\custom_textfield.dart
type nul > widgets\common\custom_button.dart
type nul > widgets\common\role_selector.dart
type nul > widgets\common\payment_status_indicator.dart
type nul > widgets\common\loading_indicator.dart

:: Widgets - Patient
type nul > widgets\patient\doctor_card.dart
type nul > widgets\patient\order_card.dart
type nul > widgets\patient\appointment_card.dart

:: Widgets - Store
type nul > widgets\patient\store\medicine_card.dart
type nul > widgets\patient\store\cart_item_widget.dart
type nul > widgets\patient\store\checkout_summary_widget.dart

:: Widgets - Doctor
type nul > widgets\doctor\prescription_form_widget.dart
type nul > widgets\doctor\patient_info_card.dart

:: Widgets - Admin
type nul > widgets\admin\user_card.dart
type nul > widgets\admin\doctor_card_admin.dart
type nul > widgets\admin\order_card_admin.dart
type nul > widgets\admin\appointment_card_admin.dart
type nul > widgets\admin\medicine_card_admin.dart

:: Utils
type nul > utils\validators.dart
type nul > utils\formatters.dart
type nul > utils\date_utils.dart
type nul > utils\device_utils.dart

:: Config
type nul > config\routes.dart
type nul > config\themes.dart
type nul > config\env.dart

:: Extensions
type nul > extensions\context_extensions.dart
type nul > extensions\string_extensions.dart

echo Medicore structure created successfully!
pause
