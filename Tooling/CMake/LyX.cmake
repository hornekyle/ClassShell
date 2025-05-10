#===========================================#
#== Find and add all LyX files under path ==#
#===========================================#

# Create top-level target
add_custom_target("LyX" ALL)

# Find all LyX files in listed search paths
file(
	GLOB_RECURSE
		LYX_FILES
	RELATIVE
		"${CMAKE_SOURCE_DIR}"
	"Documents/*.lyx"
	)

foreach(LYX_FILE ${LYX_FILES})
	# Create names and paths
	string(REPLACE ".lyx" ".pdf" PDF_FILE "${LYX_FILE}")
	string(REPLACE ".lyx" ".log" LOG_FILE "${LYX_FILE}")
	
	set(LYX_FILE_FULL "${CMAKE_SOURCE_DIR}/${LYX_FILE}")
	set(PDF_FILE_FULL "${CMAKE_BINARY_DIR}/${PDF_FILE}")
	set(LOG_FILE_FULL "${CMAKE_BINARY_DIR}/Logs/${LOG_FILE}")
	
	string(REPLACE ".lyx" "" BARE_NAME "${LYX_FILE}")
	string(REPLACE " " "" DENSE_NAME "${LYX_FILE}")
	string(REPLACE "/" "-+-" TARGET_NAME "${DENSE_NAME}")
	get_filename_component(INSTALL_DIR "${PDF_FILE}" DIRECTORY)
	
	get_filename_component(LOG_PATH_FULL "${LOG_FILE_FULL}" DIRECTORY)
	file(MAKE_DIRECTORY "${LOG_PATH_FULL}")
	
	# Find dependencies of LyX document
	execute_process(
		COMMAND
			python "${CMAKE_SOURCE_DIR}/Tooling/LyX/ListDependencies.py" "${LYX_FILE}"
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
	
	set(TARGET_ALERT " :  <source>:${LYX_FILE}\n→    <build>:${PDF_FILE}")
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
	add_custom_target("${TARGET_NAME}" ALL DEPENDS "${PDF_FILE}")
	add_dependencies("LyX" "${TARGET_NAME}")
	
	# Make conditional; don't install files with leading underscore
	get_filename_component(BASENAME ${LYX_FILE} NAME)
	if(${BASENAME} MATCHES "_.*")
		message("Skipping install of ${BASENAME}")
	else(${BASENAME} MATCHES "_.*")
		install(FILES ${PDF_FILE_FULL} DESTINATION "${INSTALL_DIR}")
	endif(${BASENAME} MATCHES "_.*")
endforeach(LYX_FILE)
