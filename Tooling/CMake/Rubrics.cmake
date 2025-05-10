#==============================#
#== Find and add all rubrics ==#
#==============================#

# Create top-level target
add_custom_target("Rubrics" ALL)

set(SCRIPT_FILE "${CMAKE_SOURCE_DIR}/Tooling/Generators/Rubrics.py")
set(RUBRICS_SHEET "Tooling/Sheets/Rubrics.ods")
set(RUBRICS_SHEET_FULL "${CMAKE_SOURCE_DIR}/${RUBRICS_SHEET}")

execute_process(
	COMMAND
		python "-B" "${SCRIPT_FILE}"
		"${RUBRICS_SHEET_FULL}" "--rubrics"
	OUTPUT_VARIABLE
		RUBRICS_LIST
	WORKING_DIRECTORY
		"${CMAKE_BINARY_DIR}"
	)

foreach(RUBRIC ${RUBRICS_LIST})
	# Set output and target names
	set(TARGET_NAME "Include-+-Rubrics-+-${RUBRIC}")
	
	set(TEX_FILE "Includes/Rubrics/${RUBRIC}.tex")
	set(TEX_FILE_FULL "${CMAKE_BINARY_DIR}/${TEX_FILE}")
	get_filename_component(TEX_PATH_FULL "${TEX_FILE_FULL}" DIRECTORY)
	file(MAKE_DIRECTORY "${TEX_PATH_FULL}")
	
	string(REPLACE ".tex" ".log" LOG_FILE "${TEX_FILE}")
	set(LOG_FILE_FULL "${CMAKE_BINARY_DIR}/Logs/${LOG_FILE}")
	get_filename_component(LOG_PATH_FULL ${LOG_FILE_FULL} DIRECTORY)
	file(MAKE_DIRECTORY "${LOG_PATH_FULL}")
	
	set(TARGET_ALERT " :  <source>:${RUBRICS_SHEET}∈${RUBRIC} →  <build>:${TEX_FILE}")
	message("${TARGET_ALERT}")
	
	# Create command to run the script and build the plots
	add_custom_command(
		OUTPUT
			"${TEX_FILE_FULL}"
		COMMAND
			date > "${LOG_FILE_FULL}"
		COMMAND
			python
			>> "${LOG_FILE_FULL}"
			"-B" "${SCRIPT_FILE}" "${RUBRICS_SHEET_FULL}"
			"--build" "${RUBRIC}" "${TEX_FILE_FULL}"
		MAIN_DEPENDENCY
			"${RUBRICS_SHEET_FULL}"
		DEPENDS
			"${SCRIPT_FILE}"
		COMMENT
			"${TARGET_ALERT}"
		WORKING_DIRECTORY
			"${CMAKE_BINARY_DIR}"
		)
		
	# Create custom target to create file with dependencies
	add_custom_target("${TARGET_NAME}" ALL DEPENDS "${TEX_FILE_FULL}")
	add_dependencies("Rubrics" "${TARGET_NAME}")
endforeach(RUBRIC ${RUBRICS_LIST})
