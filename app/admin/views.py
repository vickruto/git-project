# app/admin/views.py

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from forms import WorkshopForm,RoomForm,RoomAssignWorkshopForm
from .. import db
from ..models import Workshop,Room


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)


# Workshop Views


@admin.route('/workshops', methods=['GET', 'POST'])
@login_required
def list_workshops():
    """
    List all workshops
    """
    check_admin()

    workshops=Workshop.query.all()

    return render_template('admin/workshops/workshops.html',
                               workshops=workshops)



@admin.route('/workshops/add', methods=['GET', 'POST'])
@login_required


def add_workshop():
  """
  Add a workshop to the database
  """
  check_admin()
  add_workshop=True
  form=WorkshopForm()

  if form.validate_on_submit():
      workshop=Workshop(workshop=form.workshop.data
                        )

      try:
         #add a workshop to the database
         db.session.add(workshop)
         db.session.commit()
         flash('You have Successfully added a new workshop')

      except:
         #incase the workshop already exists
         flash('Error!Workshop already exists')

         #redirect to the workshop page

      return redirect(url_for('admin.list_workshops'))

      #loads workshop template

  return render_template('admin/workshops/workshop.html',add_workshop=add_workshop,form=form)





@admin.route('/workshops/edit/<int:workshopid>',methods=['GET','POST'])
@login_required
def edit_workshop(workshopid):
    """
    Edit a workshop
    """
    check_admin()

    add_workshop = False

    workshop=Workshop.query.get_or_404(workshopid)
    form=WorkshopForm()
    if form.validate_on_submit():
        workshop.workshop=form.workshop.data,
        workshop.date=form.date.data
        db.session.commit()
        flash('You have successfully edited the workshop.')

        # redirect to the departments page
        return redirect(url_for('admin.list_workshops'))

       #load workshop template
    return render_template('admin/workshops/workshop.html',
                      add_workshop=add_workshop,form=form,workshop=workshop)


@admin.route('/workshop/delete/<int:workshopid>', methods=['GET', 'POST'])
@login_required
def delete_workshop(workshopid):
    """
    Delete a workshop from the database
    """
    check_admin()

    workshop=Workshop.query.get_or_404(workshopid)
    db.session.delete(workshop)
    db.session.commit()
    flash('You have successfully deleted the workshop.')

    # redirect to the workshops page
    return redirect(url_for('admin.list_workshops'))

   
# Room Views

@admin.route('/rooms',methods=['GET','POST'])
@login_required
def list_rooms():
    check_admin()
    """
    List all roles
    """
    rooms = Room.query.all()
    return render_template('admin/rooms/rooms.html',rooms = rooms)

@admin.route('/rooms/add', methods=['GET', 'POST'])
@login_required
def add_room():
    """
    Add a room to the database
    """
    check_admin()

    add_room = True

    form = RoomForm()
    if form.validate_on_submit():
        room=Room(room_no=form.room_no.data,
                capacity=form.capacity.data)
        

        try:
            # add a room to the database
            db.session.add(room)
            db.session.commit()
            flash('You have successfully added a new room.')
        except:
            # in case room name already exists
            flash('Error: room has been taken')

        # redirect to the rooms page
        return redirect(url_for('admin.list_rooms'))

    # load room template
    return render_template('admin/rooms/room.html', add_room=add_room,
                           form=form, )


@admin.route('/rooms/edit/<string:roomnumber>',methods=['GET','POST'])
@login_required
def edit_room(roomnumber):
    """
    Edit a room
    """
    check_admin()

    add_room = False

    room = Room.query.get_or_404(roomnumber)
    form = RoomForm()
    if form.validate_on_submit():
        room.room_no=form.room_no.data,
        room.capacity=form.capacity.data
        db.session.add(room)
        db.session.commit()
        flash('You have successfully edited the role.')

        # redirect to the rooms page
        return redirect(url_for('admin.list_rooms'))

    form.capacity.data=room.capacity
    form.room_no.data=room.room_no
    return render_template('admin/rooms/room.html', add_room=add_room,form=form,room=room)


@admin.route('/rooms/delete/<string:roomnumber>', methods=['GET', 'POST'])
@login_required
def delete_room(roomnumber):
    """
    Delete a workshop from the database
    """
    check_admin()

    room=Room.query.get_or_404(roomnumber)
    db.session.delete(room)
    db.session.commit()
    flash('You have successfully deleted the room.')

    # redirect to the rooms page
    return redirect(url_for('admin.list_rooms'))




# WorkshopRoom Views

@admin.route('/workshoproom',methods=['GET','POST'])
@login_required
def list_rooms_workshops():
    """
    List all rooms assigned workshops
    """
    rooms=Room.query.all()
    workshops=Workshop.query.all()
    if not current_user.is_admin:
       return render_template('admin/roomworkshop/rooms_participant.html',rooms=rooms,workshops=workshops)
    else:
       return render_template('admin/roomworkshop/rooms.html',rooms=rooms)
    


@admin.route('/workshoproom/assign/<string:roomnumber>', methods=['GET', 'POST'])
@login_required
def assign_room_workshop(roomnumber):
    """
    Assign a room to a workshop
    """
    check_admin()

    room=Room.query.get_or_404(roomnumber)
    form=RoomAssignWorkshopForm()

   
    if form.validate_on_submit():
        room.workshop=form.workshop_id.data
        db.session.add(room)
        db.session.commit()
        flash('You have successfully assigned the room to the workshop.')

        # redirect to the rooms page
        return redirect(url_for('admin.list_rooms_workshops'))

    return render_template('admin/roomworkshop/roomworkshop.html',form=form,room=room)
