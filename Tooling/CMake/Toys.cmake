#==========================================#
#== Find and add all learning objectives ==#
#==========================================#

# Create top-level target
add_custom_target("Toys" ALL)

file(
	GLOB TOY_LIST
	LIST_DIRECTORIES true
	RELATIVE "${CMAKE_SOURCE_DIR}/Tooling/Toys"
	"${CMAKE_SOURCE_DIR}/Tooling/Toys/*"
	)

foreach(TOY ${TOY_LIST})
	file(
		GLOB_RECURSE TOY_FILE_LIST
		"${CMAKE_SOURCE_DIR}/Tooling/Toys/${TOY}/*"
		)
	
	# Set output and target names
	set(TARGET_NAME "Toy-+-${TOY}")
	
	set(PYZ_FILE "Toys/${TOY}.pyz")
	set(PYZ_FILE_FULL "${CMAKE_BINARY_DIR}/${PYZ_FILE}")
	get_filename_component(PATH_FULL "${PYZ_FILE_FULL}" DIRECTORY)
	file(MAKE_DIRECTORY "${PYZ_PATH_FULL}")
	
	string(REPLACE ".pyz" ".log" LOG_FILE "${PYZ_FILE}")
	set(LOG_FILE_FULL "${CMAKE_BINARY_DIR}/Logs/${LOG_FILE}")
	get_filename_component(LOG_PATH_FULL ${LOG_FILE_FULL} DIRECTORY)
	file(MAKE_DIRECTORY "${LOG_PATH_FULL}")
	
	set(TARGET_ALERT " :  <source>:${TOY} →  <build>:${PYZ_FILE}")
	message("${TARGET_ALERT}")
	
	# Create command to run the script and build the plots
	add_custom_command(
		OUTPUT
			"${PYZ_FILE_FULL}"
		COMMAND
			date > "${LOG_FILE_FULL}"
		COMMAND
			python
			>> "${LOG_FILE_FULL}"
			"-m" "zipapp"
			"-c" "${CMAKE_SOURCE_DIR}/Tooling/Toys/${TOY}"
			"-o" "${PYZ_FILE_FULL}"
			"-p" "/usr/bin/env python3"
		DEPENDS
			"${TOY_FILE_LIST}"
		COMMENT
			"${TARGET_ALERT}"
		WORKING_DIRECTORY
			"${CMAKE_BINARY_DIR}"
		)
		
	# Create custom target to create file with dependencies
	add_custom_target("${TARGET_NAME}" ALL DEPENDS "${PYZ_FILE_FULL}")
	add_dependencies("Toys" "${TARGET_NAME}")
endforeach(TOY ${TOY_LIST})
