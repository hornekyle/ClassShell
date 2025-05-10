#============================================#
#== Find and add all plot files under path ==#
#============================================#

# Create top-level target
add_custom_target("Plots" ALL)

execute_process(
	COMMAND
		python "-B" "-m" "ListPlots"
	OUTPUT_VARIABLE
		SCRIPT_CODES
	WORKING_DIRECTORY
		"${CMAKE_SOURCE_DIR}/Tooling/Plots"
	)

foreach(CODE ${SCRIPT_CODES})
	# Extract script name and set target name
	string(REPLACE "|" ";" LIST_SO "${CODE}")
	list(GET LIST_SO 0 PY_FILE)
	string(REPLACE ".pyz" "" BARE_NAME "${PY_FILE}")
	string(REPLACE "/" "-+-" TARGET_NAME "${BARE_NAME}")
	
	# Create log name and path
	string(REPLACE ".py" ".log" LOG_FILE "${PY_FILE}")
	set(LOG_FILE_FULL "${CMAKE_BINARY_DIR}/Logs/Plots/${LOG_FILE}")
	get_filename_component(LOG_PATH_FULL "${LOG_FILE_FULL}" DIRECTORY)
	file(MAKE_DIRECTORY "${LOG_PATH_FULL}")
	
	# Extract and add each output file as product
	set(TARGET_ALERT " :  <source>:${PY_FILE} →  <build>:{.svg;.pgf}")
	message("${TARGET_ALERT}")
	list(GET LIST_SO 1 LIST_OUTPUTS)
	string(REPLACE "," ";" PLOT_NAMES "${LIST_OUTPUTS}")
	set(PLOT_FILES "")
	foreach(PLOT_NAME ${PLOT_NAMES})
		list(APPEND PLOT_FILES "${CMAKE_BINARY_DIR}/Plots/${BARE_NAME}/${PLOT_NAME}.svg")
		list(APPEND PLOT_FILES "${CMAKE_BINARY_DIR}/Plots/${BARE_NAME}/${PLOT_NAME}.pgf")
		message("     ${BARE_NAME}/${PLOT_NAME}")
	endforeach(PLOT_NAME ${PLOT_NAMES})
	
	# Create command to run the script and build the plots
	add_custom_command(
		OUTPUT
			${PLOT_FILES}
		COMMAND
			date > "${LOG_FILE_FULL}"
		COMMAND
			python
			>> "${LOG_FILE_FULL}"
			"-B" "${CMAKE_SOURCE_DIR}/Tooling/Plots/SavePlots.py"
			"${PY_FILE}" "${CMAKE_BINARY_DIR}/Plots"
		MAIN_DEPENDENCY
			"${CMAKE_SOURCE_DIR}/Tooling/Plots/${PY_FILE}"
		DEPENDS
			"${CMAKE_SOURCE_DIR}/Tooling/Plots/SavePlots.py"
			"${CMAKE_SOURCE_DIR}/Tooling/Plots/FormatPlots.py"
		COMMENT
			"${TARGET_ALERT}"
		WORKING_DIRECTORY
			"${CMAKE_SOURCE_DIR}/Tooling/Plots"
		)
		
	# Create custom target to create file with dependencies
	add_custom_target("${TARGET_NAME}" ALL DEPENDS ${PLOT_FILES})
	add_dependencies("Plots" "${TARGET_NAME}")
endforeach(CODE ${SCRIPT_CODES})
