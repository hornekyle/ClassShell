#=========================#
#== Create Order target ==#
#=========================#

set(SCRIPT_FILE "${CMAKE_SOURCE_DIR}/Tooling/Generators/Order.py")
set(STUDENTS_SHEET "Processing/Students.ods")
set(STUDENTS_SHEET_FULL "${CMAKE_SOURCE_DIR}/${STUDENTS_SHEET}")

set(TEMPLATE_FILE "Tooling/Templates/Order.html")
set(TEMPLATE_FILE_FULL "${CMAKE_SOURCE_DIR}/${TEMPLATE_FILE}")

set(ORDER_FILE "order.html")
set(ORDER_FILE_FULL "${CMAKE_BINARY_DIR}/${ORDER_FILE}")

string(REPLACE ".html" ".log" LOG_FILE "${ORDER_FILE}")
set(LOG_FILE_FULL "${CMAKE_BINARY_DIR}/Logs/${LOG_FILE}")
get_filename_component(LOG_PATH_FULL ${LOG_FILE_FULL} DIRECTORY)
file(MAKE_DIRECTORY "${LOG_PATH_FULL}")

set(TARGET_ALERT " :  <source>:${STUDENTS_SHEET}∈${MODULE} →  <build>:${ORDER_FILE}")
message("${TARGET_ALERT}")

# Create command to run the script and build the plots
add_custom_command(
	OUTPUT
		"${ORDER_FILE_FULL}"
	COMMAND
		date > "${LOG_FILE_FULL}"
	COMMAND
		python
		>> "${LOG_FILE_FULL}"
		"-B" "${SCRIPT_FILE}"
		"${STUDENTS_SHEET_FULL}"
		"${TEMPLATE_FILE_FULL}"
		"${ORDER_FILE_FULL}"
	MAIN_DEPENDENCY
		"${STUDENTS_SHEET_FULL}"
	DEPENDS
		"${SCRIPT_FILE}"
		"${TEMPLATE_FILE}"
	COMMENT
		"${TARGET_ALERT}"
	WORKING_DIRECTORY
		"${CMAKE_BINARY_DIR}"
	)

# Create top-level target
add_custom_target("Order" ALL DEPENDS "${ORDER_FILE_FULL}")
