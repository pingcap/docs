#!/bin/bash

outputdir="server_help/"
help_topic_sql="${outputdir}mysql__help_topic.sql"
topic_id=1

echo "Generating help output in ${outputdir}"
echo "-- generated on $(date -u)" > ${help_topic_sql}

for statementfile in sql-statements/sql-statement-*md
do
	name=${statementfile:29}
	name=${name%.*}
	name=${name//-/ }
	description=$(pandoc -t plain ${statementfile})
	description=${description//\'/\"}
	echo "${description}" > "${outputdir}statement_${name}.txt"
	echo "-- Statement file: ${statementfile}" >> ${help_topic_sql}
	echo "INSERT INTO mysql.help_topic VALUES(${topic_id},'${name}',0,'${description}','','');" >> ${help_topic_sql}
	((topic_id++))
done

# TODO: extract per-function help from the docs
for functionfile in functions-and-operators/*md
do
	echo "-- Functions: ${statementfile}" >> ${help_topic_sql}
done

# TODO: Consider adding per-variable docs
