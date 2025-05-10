#==============================#
#== Find and add all modules ==#
#==============================#

# Create top-level target
add_custom_target("Modules" ALL)

set(SCRIPT_FILE "${CMAKE_SOURCE_DIR}/Tooling/Generators/Modules.py")

set(MODULES_SHEET "Tooling/Sheets/Modules.ods")
set(TEMPLATES_PATH "Tooling/Templates")
set(OUTPUTS_PATH "LyX")

set(MODULES_SHEET_FULL "${CMAKE_SOURCE_DIR}/${MODULES_SHEET}")
set(TEMPLATES_PATH_FULL "${CMAKE_SOURCE_DIR}/${TEMPLATES_PATH}")
set(OUTPUTS_PATH_FULL "${CMAKE_BINARY_DIR}/${OUTPUTS_PATH}")
set(FINAL_PATH_FULL "${CMAKE_BINARY_DIR}/Modules")

file(MAKE_DIRECTORY "${OUTPUTS_PATH_FULL}")
file(MAKE_DIRECTORY "${FINAL_PATH_FULL}")

set_directory_properties(PROPERTIES CMAKE_CONFIGURE_DEPENDS "${TEMPLATES_PATH_FULL}")

execute_process(
	COMMAND
		python "-B" "${SCRIPT_FILE}"
		"${MODULES_SHEET_FULL}"
		"${TEMPLATES_PATH_FULL}"
		"${OUTPUTS_PATH_FULL}"
	WORKING_DIRECTORY
		"${CMAKE_BINARY_DIR}"
	)

# Find all LyX files in listed search paths
file(
	GLOB_RECURSE
		LYX_FILES
	RELATIVE
		"${CMAKE_BINARY_DIR}/LyX"
	"${CMAKE_BINARY_DIR}/LyX/*.lyx"
	)

foreach(LYX_FILE ${LYX_FILES})
	# Create names and paths
	string(REPLACE "=" "/" LYX_PATH "${LYX_FILE}")
	string(REPLACE ".lyx" ".pdf" PDF_FILE "${LYX_PATH}")
	string(REPLACE ".lyx" ".log" LOG_FILE "${LYX_PATH}")
	
	set(LYX_FILE_FULL "${CMAKE_BINARY_DIR}/LyX/${LYX_FILE}")
	set(PDF_FILE_FULL "${CMAKE_BINARY_DIR}/Modules/${PDF_FILE}")
	set(LOG_FILE_FULL "${CMAKE_BINARY_DIR}/Logs/${LOG_FILE}")
	
	string(REPLACE ".pdf" "" BARE_NAME "${PDF_FILE}")
	string(REPLACE " " "" SHORT_NAME "${BARE_NAME}")
	string(REPLACE "/" "-+-" TARGET_NAME "${SHORT_NAME}")
	get_filename_component(INSTALL_DIR "${PDF_FILE}" DIRECTORY)
	
	get_filename_component(LOG_PATH_FULL "${LOG_FILE_FULL}" DIRECTORY)
	file(MAKE_DIRECTORY "${LOG_PATH_FULL}")
	
	# Find dependencies of LyX document
	execute_process(
		COMMAND
			python "${CMAKE_SOURCE_DIR}/Tooling/LyX/ListDependencies.py" "${LYX_FILE_FULL}"
		OUTPUT_VARIABLE
			DEPS_LIST
		WORKING_DIRECTORY
			"${CMAKE_SOURCE_DIR}"
		)
	
	execute_process(
		COMMAND
			python "${CMAKE_SOURCE_DIR}/Tooling/LyX/Authorize.py" ${LYX_FILE_FULL}
		OUTPUT_VARIABLE
			AUTHORIZED
		WORKING_DIRECTORY
			"${CMAKE_SOURCE_DIR}"
		)
	
	set(TARGET_ALERT " :  <source>:${LYX_FILE_FULL}\n⇾    <build>:${PDF_FILE_FULL}")
	message("${TARGET_ALERT}")
	foreach(DEP ${DEPS_LIST})
		message("     ${DEP}")
	endforeach(DEP)
	
	# Create command to compile LyX file
	add_custom_command(
		OUTPUT
			"${PDF_FILE_FULL}"
		COMMAND
			date > "${LOG_FILE_FULL}"
		COMMAND
			lyx
			>> "${LOG_FILE_FULL}" 2>&1
			"-E" "default"
			"${PDF_FILE_FULL}"
			"${LYX_FILE_FULL}"
		COMMAND
			qpdf
			>> "${LOG_FILE_FULL}"
			"--linearize"
			"--replace-input"
			"${PDF_FILE_FULL}"
		MAIN_DEPENDENCY
			"${LYX_FILE_FULL}"
		DEPENDS
			${DEPS_LIST}
			${AUTHORIZE_PY}
		COMMENT
			"${TARGET_ALERT}"
		WORKING_DIRECTORY
			"${CMAKE_BINARY_DIR}"
		)
		
	# Create custom target to create file with dependencies
	add_custom_target("${TARGET_NAME}" ALL DEPENDS "${PDF_FILE_FULL}")
	add_dependencies("Modules" "${TARGET_NAME}")
	
	# Make conditional; don't install files with leading underscore
	get_filename_component(BASENAME ${LYX_FILE} NAME)
	if(${BASENAME} MATCHES "_.*")
		message("Skipping install of ${BASENAME}")
	else(${BASENAME} MATCHES "_.*")
		install(FILES ${PDF_FILE_FULL} DESTINATION "${INSTALL_DIR}")
	endif(${BASENAME} MATCHES "_.*")
endforeach(LYX_FILE)
