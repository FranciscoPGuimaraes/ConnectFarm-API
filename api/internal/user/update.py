from fastapi import HTTPException
from psycopg2 import IntegrityError

from api.internal.db import connect
from api.models.UserModels import UserInQuery

async def update_team_by_number(cpf: str, update_data: UserInQuery) -> None:
    try:

        set_statement = "SET "
        update_params = {"cpf": cpf}

        if update_data.name:
            set_statement += "name = %(name)s, "
            update_params["name"] = update_data.name

        if update_data.email:
            set_statement += "email = %(email)s, "
            update_params["email"] = update_data.email

        if update_data.phone:
            set_statement += "phone = %(phone)s, "
            update_params["phone"] = update_data.phone

        if update_data.birth:
            set_statement += "birth = %(birth)s, "
            update_params["birth"] = update_data.birth

        # Remover a última vírgula da parte SET da query de atualização
        set_statement = set_statement.rstrip(", ")
        
        # Montar a query de atualização completa
        query = ""
        if set_statement != "SET":
            query = f"""
                    UPDATE user
                    {set_statement}
                    WHERE cpf = {cpf};
                    """

        # Executar a query de atualização
        with db_connect.connect() as conn:
            with conn.cursor() as cursor:
                if query:
                    cursor.execute(query, update_params)
                if cursor.rowcount == 0:
                    raise HTTPException(status_code=404, detail=f"User with cpf: {cpf} not found.")

    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))