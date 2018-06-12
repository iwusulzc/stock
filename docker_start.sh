while [ 1 ]; do
		if ps aux|grep docker |grep 8050 >/dev/null 2>&1; then
			sleep 1
		else
			service docker stop
			service docker start

			docker run -d -p 8050:8050  --add-host='eastmoney.com:61.152.229.228' scrapinghub/splash
			echo "docker start..."
		fi
done
