#==========================================#
#== Find and add all learning objectives ==#
#==========================================#

# Create top-level target
add_custom_target("Invoice" ALL)

set(SCRIPT_FILE "${CMAKE_SOURCE_DIR}/Tooling/Generators/Objectives.py")
set(OBJECTIVES_SHEET "Tooling/Sheets/Objectives.ods")
set(OBJECTIVES_SHEET_FULL "${CMAKE_SOURCE_DIR}/${OBJECTIVES_SHEET}")

execute_process(
	COMMAND
		python "-B" "${SCRIPT_FILE}"
		"${OBJECTIVES_SHEET_FULL}" "--modules"
	OUTPUT_VARIABLE
		MODULES_LIST
	WORKING_DIRECTORY
		"${CMAKE_BINARY_DIR}"
	)

foreach(MODULE ${MODULES_LIST})
	# Set output and target names
	set(TARGET_NAME "Include-+-${MODULE}-+-Invoice")
	
	set(TEX_FILE "Includes/${MODULE}/Invoice.tex")
	set(TEX_FILE_FULL "${CMAKE_BINARY_DIR}/${TEX_FILE}")
	get_filename_component(TEX_PATH_FULL "${TEX_FILE_FULL}" DIRECTORY)
	file(MAKE_DIRECTORY "${TEX_PATH_FULL}")
	
	string(REPLACE ".tex" ".log" LOG_FILE "${TEX_FILE}")
	set(LOG_FILE_FULL "${CMAKE_BINARY_DIR}/Logs/${LOG_FILE}")
	get_filename_component(LOG_PATH_FULL ${LOG_FILE_FULL} DIRECTORY)
	file(MAKE_DIRECTORY "${LOG_PATH_FULL}")
	
	set(TARGET_ALERT " :  <source>:${OBJECTIVES_SHEET}∈${MODULE} →  <build>:${TEX_FILE}")
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
			"-B" "${SCRIPT_FILE}" "${OBJECTIVES_SHEET_FULL}"
			"--invoice" "${MODULE}" "${TEX_FILE_FULL}"
		MAIN_DEPENDENCY
			"${OBJECTIVES_SHEET_FULL}"
		DEPENDS
			"${SCRIPT_FILE}"
		COMMENT
			"${TARGET_ALERT}"
		WORKING_DIRECTORY
			"${CMAKE_BINARY_DIR}"
		)
		
	# Create custom target to create file with dependencies
	add_custom_target("${TARGET_NAME}" ALL DEPENDS "${TEX_FILE_FULL}")
	add_dependencies("Invoice" "${TARGET_NAME}")
endforeach(MODULE ${MODULES_LIST})
