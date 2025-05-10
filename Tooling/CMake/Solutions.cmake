#==========================================#
#== Find and add all solutions ==#
#==========================================#

# Create top-level target
add_custom_target("Solutions")

set(SCRIPT_FILE "${CMAKE_SOURCE_DIR}/Tooling/Generators/Solutions.py")
set(TRACER_FILE "${CMAKE_SOURCE_DIR}/Tooling/Generators/Tracer.py")
set(GRAPHS_FILE "${CMAKE_SOURCE_DIR}/Tooling/Generators/Graphs.py")

execute_process(
	COMMAND
		python "-B" "${SCRIPT_FILE}"
		"--solutions" "${CMAKE_SOURCE_DIR}/Tooling/Solutions"
	OUTPUT_VARIABLE
		SOLUTIONS_LIST
	WORKING_DIRECTORY
		"${CMAKE_BINARY_DIR}"
	)

foreach(SOLUTION ${SOLUTIONS_LIST})
	file(
		GLOB_RECURSE SOLUTION_FILE_LIST
		"${CMAKE_SOURCE_DIR}/Tooling/Solutions/${SOLUTION}/*"
		)

	# Set output and target names
	set(TARGET_NAME "Solution-+-${SOLUTION}")
	
	set(INPUT "${CMAKE_SOURCE_DIR}/Tooling/Solutions/${SOLUTION}")
	
	set(OUTPUT "Solutions/${SOLUTION}")
	set(OUTPUT_FULL "${CMAKE_BINARY_DIR}/${OUTPUT}")
	file(MAKE_DIRECTORY "${OUTPUT_FULL}")
	
	set(LOG_FILE "Solutions/${SOLUTION}.log")
	set(LOG_FILE_FULL "${CMAKE_BINARY_DIR}/Logs/${LOG_FILE}")
	get_filename_component(LOG_PATH_FULL ${LOG_FILE_FULL} DIRECTORY)
	file(MAKE_DIRECTORY "${LOG_PATH_FULL}")
	
	file(
		GLOB SOLUTION_DIR_LIST
		LIST_DIRECTORIES true
		RELATIVE "${CMAKE_SOURCE_DIR}/Tooling/Solutions/${SOLUTION}/"
		"${CMAKE_SOURCE_DIR}/Tooling/Solutions/${SOLUTION}/*"
		)
	
	set(TARGET_ALERT " :  <source>:${SOLUTION} →  <build>:${OUTPUT}")
	message("${TARGET_ALERT}")
	
	# Create command to run the script
	add_custom_command(
		OUTPUT
			"${OUTPUT_FULL}/trace.pkl"
		COMMAND
			date > "${LOG_FILE_FULL}"
		COMMAND
			python
			>> "${LOG_FILE_FULL}"
			"-B" "${SCRIPT_FILE}"
			"--trace" "${INPUT}" "${OUTPUT_FULL}/trace.pkl"
		DEPENDS
			"${SCRIPT_FILE}"
			"${TRACER_FILE}"
			${SOLUTION_FILE_LIST}
		COMMENT
			"${TARGET_ALERT}"
		WORKING_DIRECTORY
			"${CMAKE_BINARY_DIR}"
		)
	
	# Create command to run the script
	list(TRANSFORM SOLUTION_DIR_LIST APPEND ".dot" OUTPUT_VARIABLE SOLUTION_DOT_LIST)
	list(TRANSFORM SOLUTION_DOT_LIST PREPEND "${OUTPUT_FULL}/")
	add_custom_command(
		OUTPUT
			${SOLUTION_DOT_LIST}
		COMMAND
			python
			>> "${LOG_FILE_FULL}"
			"-B" "${SCRIPT_FILE}"
			"--callgraphs" "${OUTPUT_FULL}/trace.pkl" "${OUTPUT_FULL}"
		DEPENDS
			"${OUTPUT_FULL}/trace.pkl"
			"${SCRIPT_FILE}"
			"${GRAPHS_FILE}"
		COMMENT
			"${TARGET_ALERT}"
		WORKING_DIRECTORY
			"${CMAKE_BINARY_DIR}"
		)
	
	# Create command to run the script
	list(TRANSFORM SOLUTION_DIR_LIST APPEND ".tex" OUTPUT_VARIABLE SOLUTION_TEX_LIST)
	list(TRANSFORM SOLUTION_TEX_LIST PREPEND "${OUTPUT_FULL}/")
	add_custom_command(
		OUTPUT
			${SOLUTION_TEX_LIST}
		COMMAND
			python
			>> "${LOG_FILE_FULL}"
			"-B" "${SCRIPT_FILE}"
			"--latex" "${OUTPUT_FULL}/trace.pkl" "${OUTPUT_FULL}"
		DEPENDS
			"${OUTPUT_FULL}/trace.pkl"
			"${SCRIPT_FILE}"
		COMMENT
			"${TARGET_ALERT}"
		WORKING_DIRECTORY
			"${CMAKE_BINARY_DIR}"
		)
	
	# Create custom target to create file with dependencies
	add_custom_target(
		"${TARGET_NAME}"
		DEPENDS
			${SOLUTION_DOT_LIST}
			${SOLUTION_TEX_LIST}
		)
	add_dependencies("Solutions" "${TARGET_NAME}")
endforeach(SOLUTION ${SOLUTIONS_LIST})
