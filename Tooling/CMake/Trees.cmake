#==========================================#
#== Find and add all learning objectives ==#
#==========================================#

# Create top-level target
add_custom_target("Trees" ALL)

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
	set(TARGET_NAME "Include-+-${MODULE}-+-Tree")
	
	set(DOT_FILE "Includes/${MODULE}/Tree.dot")
	set(DOT_FILE_FULL "${CMAKE_BINARY_DIR}/${DOT_FILE}")
	get_filename_component(DOT_PATH_FULL "${DOT_FILE_FULL}" DIRECTORY)
	file(MAKE_DIRECTORY "${DOT_PATH_FULL}")
	
	string(REPLACE ".dot" ".log" LOG_FILE "${DOT_FILE}")
	set(LOG_FILE_FULL "${CMAKE_BINARY_DIR}/Logs/${LOG_FILE}")
	get_filename_component(LOG_PATH_FULL ${LOG_FILE_FULL} DIRECTORY)
	file(MAKE_DIRECTORY "${LOG_PATH_FULL}")
	
	set(TARGET_ALERT " :  <source>:${OBJECTIVES_SHEET}∈${MODULE} →  <build>:${DOT_FILE}")
	message("${TARGET_ALERT}")
	
	# Create command to run the script and build the plots
	add_custom_command(
		OUTPUT
			"${DOT_FILE_FULL}"
		COMMAND
			date > "${LOG_FILE_FULL}"
		COMMAND
			python
			>> "${LOG_FILE_FULL}"
			"-B" "${SCRIPT_FILE}" "${OBJECTIVES_SHEET_FULL}"
			"--tree" "${MODULE}" "${DOT_FILE_FULL}"
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
	add_custom_target("${TARGET_NAME}" ALL DEPENDS "${DOT_FILE_FULL}")
	add_dependencies("Trees" "${TARGET_NAME}")
endforeach(MODULE ${MODULES_LIST})
