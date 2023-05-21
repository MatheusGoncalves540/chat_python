def StartThreads(thread_receber,thread_enviar):
    thread_receber.start()
    thread_enviar.start()

    thread_enviar.join()
    thread_receber.join()