from AI.app_state import State


class Prompt:
    CATEGORY_DEFINITION_PROMPT = f"""
                        Ти – система класифікації мети збору коштів.
                         Твоя задача – класифікувати мету збору до однієї з наступних категорій: 
                        {', '.join(State.CATEGORIES)}
                        РЕБ це радіо-електронна боротьба.
                        Мета збору: "{{text}}"
        
                        Вибери одну категорію, яка найбільше підходить,
                        і напиши її одним словом без додаткових коментарів.
                        Врахуй що тематика переважно військового характеру
                        """

    FINDING_COMMON_CONTEXT_PROMPT = f"""
                    Ти отримаєш перелік завдань у вигляді списку. Твоє завдання — витягнути спільний контекст,
                    якщо він існує. Контекст може включати час виконання завдань, конкретні суми донатів, категорії
                    пожертв або інші повторювані елементи. Якщо спільного контексту немає, напиши "Контекст відсутній".
        
                    **Приклад завдань:**
                    1. Зроби донат на гуманітарну допомогу зранку (7:00-9:00) та отримай 20 монет.
                    2. Пожертвуй до 9:00 ранку на категорію 'інше' та зароби 15 монет.
                    3. Поділись у соцмережах про свій донат на підтримку радіо-боротьби виконаний зранку та зароби 20 монет.
        
                    **Відповідь**: Ранкові донати та соціальна активність.
        
                    Якщо сума або час часто повторюються — це теж вважається контекстом.
        
                    Завдання: {{text}}
        
                    Відповідь дай коротку, пару слів
                    """

    CREATING_NEW_TASKS_PROMPT = f"""
                    Ти маєш створювати завдання для платформи донатів, де користувачі виконують різні завдання та отримують
                    за це монети. Кожне завдання має бути коротким, але різноманітним і цікавим, з максимальним контекстом
                    та творчістю. Наприклад, користувач може запросити друга, зробити пожертву у певний час доби або на
                    конкретну категорію, і за це отримує нагороду у вигляді монет.
        
                    **Контекст:**
                    Це основний контекст на основі якого потрібно створювати завдання. КОНТЕКСТ: '{{text}}'.
                    Основний акцент має бути саме на контексті який я вказав вище.
                     Контекст має фігурувати в завданнях обовязково
                    1. Кожне завдання має бути унікальним, не повторюватися.
                    2. Завдання можуть бути прив’язані до різних категорій, але не обов’язково кожен раз.
                    3. Використовуй різні моменти дня (зранку, після обіду, ввечері тощо),
                     завуальовуй ці моменти для різноманітності.
                    4. Завдання можуть бути на суму (наприклад, донат сумарно 1000 грн за тиждень).
                    5. Завдання можуть включати соціальну активність (наприклад, запроси друга, поділись у соцмережах).
                    6. Категорії, до яких можуть бути прив'язані завдання:
                       {','.join(State.CATEGORIES)}
        
                    **Приклади завдань:**
                    1. Запроси друга на платформу та отримай 20 монет.
                    2. Задонать на освіту о 8:30 ранку та зароби 15 монет.
                    3. Пожертвуй сумарно 1000 грн цього тижня на медицину та отримай 30 монет.
                    4. Поділись своїм збором у соцмережах і отримай 10 монет.
                    5. Зроби донат рівно 100 грн на підтримку піхоти та отримай 25 монет.
                    6. Пожертвуй до 10:00 ранку на транспорт і зароби 20 монет.
                    7. Задонать на їжу після обіду (14:00-18:00) та отримай 15 монет.
                    8. Зроби третій донат за тиждень і зароби 20 монет.
                    9. Пожертвуй на дрони та комплектуючі на суму 200 грн або більше і отримай 25 монет.
                    10. Запроси двох друзів задонатити разом і зароби 30 монет.
                    Це тільки приклади завдань, основне правило - дотримуватись контексту, це дуже важливо.
                    Також завдання можуть бути легкі середні та складні, врахуй це, та випадково створюй. 
        
                    Генеруй 3 нові завдання на основі цього прикладу. Пиши тільки завдання, нічого зайвого.
                    Кожного разу цифри повинні бути 1. 2. 3
                    """

    SEARCH_BEHAVIORAL_PATTERN_PROMPT = f""" Твоя задача отримувати вхідні дані і відповідно до них зрозуміти коли як і чому людина 
                                     донатить на Збройні Сили України. Можливо це прив'язка до дня зарплати, можливо це 
                                     донат людини лише знайомим або по якомусь конкретному регіону України чи ще щось. 
                                     В результаті важливо отримати саме конкретну інформацію чому людина донатить.
                                     Приклад вхідних даних:
                                     Донат на херсон, Донат на медикаменти, Донат на лікарню 'Охмадит'
                                     Приклад бажаної відповіді: Емоційний зв’язок з регіоном або конкретною метою (Херсон — підтримка рідного регіону, медикаменти — гуманітарна допомога, лікарня Охмадит — допомога дітям).
                                     
                                     Ось мої реальні вхідні дані
                                     Вхідні дані: {{text}}
                                     Чекаю відповіді.
                                """

