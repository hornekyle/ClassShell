#===========================================#
#== Find and add all LyX files under path ==#
#===========================================#

# Create top-level target
add_custom_target("Typst" ALL)

# Find all Typst files in listed search paths
file(
	GLOB_RECURSE
		TYP_FILES
	RELATIVE
		"${CMAKE_SOURCE_DIR}"
	"Documents/*.typ"
	)

foreach(TYP_FILE ${TYP_FILES})
	# Create names and paths
	string(REPLACE ".typ" ".pdf" PDF_FILE "${TYP_FILE}")
	string(REPLACE ".typ" ".log" LOG_FILE "${TYP_FILE}")
	
	set(TYP_FILE_FULL "${CMAKE_SOURCE_DIR}/${TYP_FILE}")
	set(PDF_FILE_FULL "${CMAKE_BINARY_DIR}/${PDF_FILE}")
	set(LOG_FILE_FULL "${CMAKE_BINARY_DIR}/Logs/${LOG_FILE}")
	
	string(REPLACE ".typ" "" BARE_NAME "${TYP_FILE}")
	string(REPLACE " " "" DENSE_NAME "${TYP_FILE}")
	string(REPLACE "/" "-+-" TARGET_NAME "${DENSE_NAME}")
	get_filename_component(INSTALL_DIR "${PDF_FILE}" DIRECTORY)
	
	get_filename_component(LOG_PATH_FULL "${LOG_FILE_FULL}" DIRECTORY)
	file(MAKE_DIRECTORY "${LOG_PATH_FULL}")
	
	set(TARGET_ALERT " :  <source>:${TYP_FILE}\n→    <build>:${PDF_FILE}")
	message("${TARGET_ALERT}")
	
	# Create command to compile LyX file
	add_custom_command(
		OUTPUT
			"${PDF_FILE_FULL}"
		COMMAND
			date > "${LOG_FILE_FULL}"
		COMMAND
			typst compile
			--root ${CMAKE_SOURCE_DIR}
			--jobs 1
			>> "${LOG_FILE_FULL}" 2>&1
			"${TYP_FILE_FULL}"
			"${PDF_FILE_FULL}"
		COMMAND
			qpdf
			>> "${LOG_FILE_FULL}"
			"--linearize"
			"--replace-input"
			"${PDF_FILE_FULL}"
		MAIN_DEPENDENCY
			"${TYP_FILE_FULL}"
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
	add_dependencies("Typst" "${TARGET_NAME}")
	
	# Make conditional; don't install files with leading underscore
	get_filename_component(BASENAME ${TYP_FILE} NAME)
	if(${BASENAME} MATCHES "_.*")
		message("Skipping install of ${BASENAME}")
	else(${BASENAME} MATCHES "_.*")
		install(FILES ${PDF_FILE_FULL} DESTINATION "${INSTALL_DIR}")
	endif(${BASENAME} MATCHES "_.*")
endforeach(TYP_FILE)
